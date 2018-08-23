from typing import List, Dict, Optional, Set
import subprocess
import os.path
# import argparse

debug = False
def DEBUG_PRINT(msg: str):
  if debug:
    print(msg)

#  A rule consists of three parts: the target, its prerequisites, and the command(s) to perform:
class Rule:
    def __init__(self, target: str, prereqs: List[str], commands: List[str]) -> None:
        # prereq is a string that can be either a file name, a target for another rule, or both
        self.prereqs = prereqs
        # target can be a file name, but doesn't have to
        self.target = target
        # shell commans to execute when the rule gets executed
        self.commands = commands
        # true if this rule has been executed
        self.updated = False

    def execute(self) -> None:
      for command in self.commands:
        DEBUG_PRINT("[`{}` exec] {}".format(self.target, command))
        print(command)
        retcode = subprocess.call(command,shell=True)
        if retcode != 0:
          raise ValueError("[{}] Error {}".format(self.target, retcode))

        self.updated = True

    def __repr__(self):
      return "Rule(target={}, prereqs={}, commands={})".format(self.target, self.prereqs, self.commands)


def file_exists(name: str) -> bool:
  if os.path.islink(name):
    return True
  val = os.path.isfile(name)
  if val:
    DEBUG_PRINT("{} exists as a file".format(name))
  return val

def is_newer(file1: str, file2: str):
  newer = os.path.getmtime(file1) >=  os.path.getmtime(file2)
  if newer:
    DEBUG_PRINT("{} is newer than {}".format(file1, file2))
  else:
    DEBUG_PRINT("{} is NOT newer than {}".format(file1, file2))
  return newer


def traverse_dependencies(root: Rule, rule_map: Dict[str, Rule]) -> List[Rule]:
  ''' perform level order traversal of the tree, starting at root. This ensures that a rule will always appear before its pre-requisites.
  '''
  level_order: List[Rule] = [root]
  visited: Set[Rule] = set() # useful for detecting circular dependencies
  index = 0
  while index < len(level_order):
    cur = level_order[index]
    visited.add(cur)
    for prereq in cur.prereqs:
      if prereq not in rule_map and not file_exists(prereq):
        raise ValueError("*** No rule to make target `{}', needed by `{}'. Stop.".format(prereq, cur.target))

      if prereq in rule_map:
        prereq_rule = rule_map[prereq]
        if prereq_rule in visited:
          print("make: Circular {} <- {} dependency dropped.".format(cur.target, prereq))
        else:
          level_order.append(rule_map[prereq])
          visited.add(rule_map[prereq])

    index += 1
  return level_order

def execute_rules(rules: List[Rule]):
  if not rules:
    return
  root = rules[0]

  rule_map: Dict[str, Rule] = {x.target: x for x in rules}
  DEBUG_PRINT("rule_map: {}".format(rule_map))

  eval_order = reversed(traverse_dependencies(root, rule_map))

  # eval_order ensures that rule's dependencies are considered before the rule itself
  for rule in eval_order:
    DEBUG_PRINT("now executing rule: {}".format(rule))

    # a rule whose target doesn't exist always gets executed
    if not file_exists(rule.target):
      rule.execute()
      continue

    for prereq in rule.prereqs:
      DEBUG_PRINT("considering prereq: {}".format(prereq))

      if prereq in rule_map:
        prereq_rule = rule_map[prereq]
        if prereq_rule.updated or is_newer(prereq_rule.target, rule.target):
          rule.execute()
          break
      elif is_newer(prereq, rule.target):
          rule.execute()
          break

  if not root.updated:
    print("'{}' is up to date".format(root.target))


def parse_rules(makefile_content: str) -> List[Rule]:
  result: List[Rule] = []

  lines = makefile_content.split('\n')
  current_rule: Optional[Rule] = None
  for num, line in enumerate(lines):
    DEBUG_PRINT("{}:{}".format(num, line))
    if not line: # skip empty lines
      continue
    if line[0] == '\t' or line.startswith("    "):
      if not current_rule:
        raise ValueError("syntax error at line {}: ".format(num))
      current_rule.commands.append(line.strip())
      continue

    parts = line.strip().split(":")
    if len(parts) != 2:
      raise ValueError("syntax error at target prereqs specification. line {}".format(num))
    target, prereqs_raw = parts
    prereqs = prereqs_raw.strip().split(" ") if prereqs_raw else []
    current_rule = Rule(target, prereqs, [])
    result.append(current_rule)

  return result


makefile="""
build: judge loco
        echo "building build..."
        touch build
judge: caca
        echo "building judge"
        touch judge
caca: build
        echo "caca"
"""

if __name__ == '__main__':
  rules = parse_rules(makefile)
  DEBUG_PRINT("parsed rules: {}".format(rules))
  execute_rules(rules)

