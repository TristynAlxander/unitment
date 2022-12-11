# Header
if(True):
  __doc__          = "This module contains unit tests. Passed 0.0.1"
  __version__      = "0.0.1"
  __reverse_path__ = "../"
  
  # Python Standard Imports
  import sys, os
  
  # Python Math Imports
  if(True):
    import math,cmath,random
    from decimal import *
    from numbers import Number
  
  # Logging Functions
  if(True):
    import logging, types
    
    global log
    log = logging.getLogger()
    
    def log_func(func,context,name=None):
      # Simplify Variables
      name = name if(name!=None) else func.__name__
      # Context: Extend for Non-Nested, Replace for Nested
      if(log.name == "root"): context = context  + "." + name
      else:                   context = log.name + "." + name
      context = ".".join([_.strip("_") for _ in context.split(".")])
      # Wrappers to Update Context
      def log_wrapper(*args, **kwargs):
        # Log with Context
        global log
        log = logging.getLogger(context)
        out = func(*args, **kwargs)
        log = logging.getLogger()
        return out 
      # Return Wrapped Function
      return log_wrapper
    def log_class(cls,context):
      # Add Context
      context = context + "." + cls.__name__
      # Iterate over class dict
      for name, obj in vars(cls).items():
        is_function = callable(obj) and not isinstance(obj,type)
        is_class    = callable(obj) and     isinstance(obj,type)
        if(is_function): setattr( cls, name, log_func( obj,context,name=name) )
        if(is_class):    setattr( cls, name, log_class(obj,context) )
      return cls
    def log_this(obj,context=None):
      # Initial Context
      if(context==None):context = __name__
      # Sort
      is_function = callable(obj) and not isinstance(obj,type)
      is_class    = callable(obj) and     isinstance(obj,type)
      # Return
      if(is_function): return log_func( obj,context)
      if(is_class):    return log_class(obj,context)
  
  # Repo-Script for Repo-Imports
  if(True):
    # Define Repo-Library Path.
    _file_dir_     = os.path.dirname(__file__)
    _repo_dir_     = os.path.join(_file_dir_, __reverse_path__)
    _repo_lib_dir_ = os.path.join(_repo_dir_, "src/")
    _repo_lib_dir_ = os.path.normpath(_repo_lib_dir_)
    # Add Repo-Library to Path.
    if(_repo_lib_dir_ not in sys.path): sys.path.insert(0, _repo_lib_dir_)
  
  # Additional Imports
  import pytest
  from unitment import AmbiguousUnitException,IncompatibleUnitException,UnitException,Unit,Measure
  import unitment as measure

# To-Do add Numpy Tests
# https://numpy.org/doc/stable/reference/ufuncs.html

# Units
"""
from tests.maths.measure.unit_init import *
from tests.maths.measure.unit_str  import *
from tests.maths.measure.unit_op   import *
# Measures
from tests.maths.measure.meas_init import *
from tests.maths.measure.meas_str  import *
from tests.maths.measure.meas_op   import *
#"""
# Testing Protocol 
# pytest tests/maths/measure.py
# coverage run -m pytest tests/maths/measure.py
# coverage report -m 

class TestUnit:
  # If this is failing you have init problems. 
  if(True): UNITS = (
    Unit(["u"]),Unit(["u","u"]),Unit(["ua","ub","ub"]),
    Unit(["nu"],["du"]),Unit(["nu","nu","nu"],["du","du"]),Unit(["nua","nub","nub"],["dua","dub","dub","dub"]),
    Unit(["u"],10.1),Unit(["u","u"],10.1),Unit(["ua","ub","ub"],10.1),
    Unit(["nu"],["du"],10.1),Unit(["nu","nu","nu"],["du","du"],10.1),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],10.1),
    Unit(["u"],10e1),Unit(["u","u"],10e1),Unit(["ua","ub","ub"],10e1),
    Unit(["nu"],["du"],10e1),Unit(["nu","nu","nu"],["du","du"],10e1),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],10e1),
    Unit(["u"],-10.1),Unit(["u","u"],-10.1),Unit(["ua","ub","ub"],-10.1),
    Unit(["nu"],["du"],-10.1),Unit(["nu","nu","nu"],["du","du"],-10.1),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],-10.1),
    Unit(["u"],-10e1),Unit(["u","u"],-10e1),Unit(["ua","ub","ub"],-10e1),
    Unit(["nu"],["du"],-10e1),Unit(["nu","nu","nu"],["du","du"],-10e1),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],-10e1),
    Unit(["u"],"10.1"),Unit(["u","u"],"10.1"),Unit(["ua","ub","ub"],"10.1"),
    Unit(["nu"],["du"],"10.1"),Unit(["nu","nu","nu"],["du","du"],"10.1"),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],"10.1"),
    Unit(["u"],"10e1"),Unit(["u","u"],"10e1"),Unit(["ua","ub","ub"],"10e1"),
    Unit(["nu"],["du"],"10e1"),Unit(["nu","nu","nu"],["du","du"],"10e1"),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],"10e1"),
    Unit(["u"],"-10.1"),Unit(["u","u"],"-10.1"),Unit(["ua","ub","ub"],"-10.1"),
    Unit(["nu"],["du"],"-10.1"),Unit(["nu","nu","nu"],["du","du"],"-10.1"),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],"-10.1"),
    Unit(["u"],"-10e1"),Unit(["u","u"],"-10e1"),Unit(["ua","ub","ub"],"-10e1"),
    Unit(["nu"],["du"],"-10e1"),Unit(["nu","nu","nu"],["du","du"],"-10e1"),Unit(["nua","nub","nub"],["dua","dub","dub","dub"],"-10e1"),
    Unit(10),Unit(-10),Unit(10.1),Unit(10e1),Unit(-10.1),Unit(-10e1),
    Unit("10.1"),Unit("10e1"),Unit("-10.1"),Unit("-10e1"),
    Unit(Decimal("10.1")),Unit(Decimal("10e1")),Unit(Decimal("-10.1")),Unit(Decimal("-10e1")),
    )
  else: UNITS = ()
  
class TestPracticals:
  # Assorted Past Failures
  def test_failures(self):
    # Past Failed Units
    pass
  # Exact Unit Conversion.
  def test_conversion_constants(self):
    
    # Pound (lb,lbf), Inch (in), psi Definitions
    lbf = Measure("1 lbf",Unit.IMPERIAL_UNITS)
    in2 = Measure("1 in^2",Unit.IMPERIAL_UNITS)
    psi = (lbf/in2).convert("psi",Unit.PRESSURE_UNITS)
    assert psi.value == 1
    
    # Distance
    assert Measure("12 in",Unit.IMPERIAL_UNITS).convert("ft",Unit.IMPERIAL_UNITS).value == 1
    assert Measure("12 in",Unit.IMPERIAL_UNITS).convert(Unit("ft",Unit.IMPERIAL_UNITS)).value == 1
  
  def test_challenge_problems(self):
    assert Measure("10 K^-1") * Unit("\u00B0F",definitions = Unit.IMPERIAL_UNITS) == Decimal("2559.277777777777777777777778")