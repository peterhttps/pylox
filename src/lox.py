import sys
from interpreter import Interpreter
from scanner import *
from parserC import ParserC
from ast_printer import AstPrinter

class Lox: 
  def __init__(self):
    self.hadError = False

  def main(self, args: list[str]):
    if (len(args) > 2):
      print("Usage: pylox [script]")
      sys.exit()
    elif (len(args) == 2):
      self.runFile(args[1])
    else:
      self.runPrompt()
    
  def runFile(self, path):
    file = open(path, mode='r')
    allText = file.read()
    self.run(allText)
    if (self.hadError):
      sys.exit()

  def runPrompt(self):
    while True:
      line = input("> ")
      if (line == "exit()"):
        break
      self.run(line)
      self.hadError = False

  def run(self, source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    parser = ParserC(tokens)
    statements = parser.parse()
    interpreter = Interpreter()

    if (self.hadError):
      return

    interpreter.interpret(statements)

  def error(self, line: int, message: str):
    self.report(line, "", message)

  def report(self, line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}")
    self.hadError = True