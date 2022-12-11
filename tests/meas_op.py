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

class TestMeasureOperators:
  
  # Equality
  def test_approx(self):
    assert not Measure("21(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("22(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("23(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("24(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("25(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("26(1)e4cm").approx(Measure("24(1)e4cm"))
    assert not Measure("27(1)e4cm").approx(Measure("24(1)e4cm"))
    assert     Measure("5").approx(5)
    assert     Measure("5").approx(Decimal("5"))
    assert     Measure("5 m^2",value="2").approx(Measure("10m^2"))
    with pytest.raises(IncompatibleUnitException):
      Measure("12 mg").approx(Measure("12 uL"))
  def test_eq(self):
    # Units
    assert Measure("24(1)e4cm") == Measure("24(1)e4cm")
    assert Measure("0.64(5)m")  == Measure("64(5)cm")
    assert Measure("5 m^2",value="2") == Measure("10 m^2")
    # unitless 
    assert Measure("24(1)e4") == Measure("24(1)e4")
    assert Measure("5") == Measure(5)
    assert Measure("5") == Decimal("5")
    assert Measure("3000") != True
    # Float Flexibility
    assert Measure(value=2.5,units=None).value == Decimal("2.5")
  def test_ne(self):
    # To-DO Internal Types Don't Matter for equals
    # assert Measure(units="cm", value= 12.4, error=6.2) == Measure(units="cm", value= Decimal("12.4"), error=Decimal("6.2"))
    
    assert Measure("0.64(5)m")  != Measure("64(5)m")
    assert Measure("5") != Measure(1)
    assert Measure("5") != Decimal("1")
    assert Measure("5 m^2",value="2") != Measure("2 m^2")
  
  # Relative
  def test_lt(self):
    # No Uncertainty
    if(True):
      # Units
      assert     Measure("23e4cm") < Measure("24e4cm")
      assert not Measure("24e4cm") < Measure("24e4cm")
      assert not Measure("25e4cm") < Measure("24e4cm")
      # Unitless
      assert     Measure("23e4") < Measure("24e4")
      assert not Measure("24e4") < Measure("24e4")
      assert not Measure("25e4") < Measure("24e4")
      # Decimal 
      assert     Measure("23e4") < Measure("24e4")
      assert not Measure("24e4") < Measure("24e4")
      assert not Measure("25e4") < Measure("24e4")
      # Magnitude
      assert     Measure("5 m^2",value="2") < Measure("11 m^2")
      assert not Measure("5 m^2",value="2") < Measure("10 m^2")
      assert not Measure("5 m^2",value="2") < Measure("9 m^2")
    # Uncertainty
    if(True):
      # Units
      assert     Measure("21(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("22(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("23(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("24(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("25(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("26(1)e4cm") < Measure("24(1)e4cm")
      assert not Measure("27(1)e4cm") < Measure("24(1)e4cm")
      # Unitless 
      assert     Measure("21(1)e4") < Measure("24(1)e4")
      assert not Measure("22(1)e4") < Measure("24(1)e4")
      assert not Measure("23(1)e4") < Measure("24(1)e4")
      assert not Measure("24(1)e4") < Measure("24(1)e4")
      assert not Measure("25(1)e4") < Measure("24(1)e4")
      assert not Measure("26(1)e4") < Measure("24(1)e4")
      assert not Measure("27(1)e4") < Measure("24(1)e4")
    # UnitExceptions 
    if(True):
      with pytest.raises(IncompatibleUnitException):
        Measure("12 mg") < Measure("12 uL")
  def test_le(self):
    # No Uncertainty
    if(True):
      # units
      assert     Measure("23e4cm") <= Measure("24e4cm")
      assert     Measure("24e4cm") <= Measure("24e4cm")
      assert not Measure("25e4cm") <= Measure("24e4cm")
      # unitless
      assert     Measure("23e4") <= Measure("24e4")
      assert     Measure("24e4") <= Measure("24e4")
      assert not Measure("25e4") <= Measure("24e4")
      # Decimal
      assert     Measure("23e4") <= Decimal("24e4")
      assert     Measure("24e4") <= Decimal("24e4")
      assert not Measure("25e4") <= Decimal("24e4")
      # Magnitude
      assert     Measure("5 m^2",value="2") <= Measure("11 m^2")
      assert     Measure("5 m^2",value="2") <= Measure("10 m^2")
      assert not Measure("5 m^2",value="2") <= Measure("9 m^2")
    # Uncertainty
    if(True):
      # Units
      assert     Measure("21(1)e4cm") <= Measure("24(1)e4cm")
      assert     Measure("22(1)e4cm") <= Measure("24(1)e4cm")
      assert     Measure("23(1)e4cm") <= Measure("24(1)e4cm")
      assert     Measure("24(1)e4cm") <= Measure("24(1)e4cm")
      assert not Measure("25(1)e4cm") <= Measure("24(1)e4cm")
      assert not Measure("26(1)e4cm") <= Measure("24(1)e4cm")
      assert not Measure("27(1)e4cm") <= Measure("24(1)e4cm")
      # Unitless
      assert     Measure("21(1)e4") <= Measure("24(1)e4")
      assert     Measure("22(1)e4") <= Measure("24(1)e4")
      assert     Measure("23(1)e4") <= Measure("24(1)e4")
      assert     Measure("24(1)e4") <= Measure("24(1)e4")
      assert not Measure("25(1)e4") <= Measure("24(1)e4")
      assert not Measure("26(1)e4") <= Measure("24(1)e4")
      assert not Measure("27(1)e4") <= Measure("24(1)e4")
    # UnitExceptions 
    if(True):
      with pytest.raises(IncompatibleUnitException):
        Measure("12 mg") <= Measure("12 uL")
  def test_gt(self):
    # No Uncertainty
    if(True):
      # Units 
      assert not Measure("23e4cm") > Measure("24e4cm")
      assert not Measure("24e4cm") > Measure("24e4cm")
      assert     Measure("25e4cm") > Measure("24e4cm")
      # Unitless
      assert not Measure("23e4") > Measure("24e4")
      assert not Measure("24e4") > Measure("24e4")
      assert     Measure("25e4") > Measure("24e4")
      # Decimal
      assert not Measure("23e4") > Decimal("24e4")
      assert not Measure("24e4") > Decimal("24e4")
      assert     Measure("25e4") > Decimal("24e4")
      # Magnitude
      assert not Measure("5 m^2",value="2") > Measure("11 m^2")
      assert not Measure("5 m^2",value="2") > Measure("10 m^2")
      assert     Measure("5 m^2",value="2") > Measure("9 m^2")
    # Uncertainty
    if(True):
      # Units
      assert not Measure("21(1)e4cm") > Measure("24(1)e4cm")
      assert not Measure("22(1)e4cm") > Measure("24(1)e4cm")
      assert not Measure("23(1)e4cm") > Measure("24(1)e4cm")
      assert not Measure("24(1)e4cm") > Measure("24(1)e4cm")
      assert not Measure("25(1)e4cm") > Measure("24(1)e4cm")
      assert not Measure("26(1)e4cm") > Measure("24(1)e4cm")
      assert     Measure("27(1)e4cm") > Measure("24(1)e4cm")
      # Unitless
      assert not Measure("21(1)e4") > Measure("24(1)e4")
      assert not Measure("22(1)e4") > Measure("24(1)e4")
      assert not Measure("23(1)e4") > Measure("24(1)e4")
      assert not Measure("24(1)e4") > Measure("24(1)e4")
      assert not Measure("25(1)e4") > Measure("24(1)e4")
      assert not Measure("26(1)e4") > Measure("24(1)e4")
      assert     Measure("27(1)e4") > Measure("24(1)e4")
    # UnitExceptions 
    if(True):
      with pytest.raises(IncompatibleUnitException):
        Measure("12 mg") > Measure("12 uL")
  def test_ge(self):
    # No Uncertainty
    if(True):
      # Units
      assert not Measure("23e4cm") >= Measure("24e4cm")
      assert     Measure("24e4cm") >= Measure("24e4cm")
      assert     Measure("25e4cm") >= Measure("24e4cm")
      # Unitless
      assert not Measure("23e4") >= Measure("24e4")
      assert     Measure("24e4") >= Measure("24e4")
      assert     Measure("25e4") >= Measure("24e4")
      # Decimal
      assert not Measure("23e4") >= Decimal("24e4")
      assert     Measure("24e4") >= Decimal("24e4")
      assert     Measure("25e4") >= Decimal("24e4")
      # Magnitude
      assert not Measure("5 m^2",value="2") >= Measure("11 m^2")
      assert     Measure("5 m^2",value="2") >= Measure("10 m^2")
      assert     Measure("5 m^2",value="2") >= Measure("9 m^2")
    # Uncertainty
    if(True):
      # Units
      assert not Measure("21(1)e4cm") >= Measure("24(1)e4cm")
      assert not Measure("22(1)e4cm") >= Measure("24(1)e4cm")
      assert not Measure("23(1)e4cm") >= Measure("24(1)e4cm")
      assert     Measure("24(1)e4cm") >= Measure("24(1)e4cm")
      assert     Measure("25(1)e4cm") >= Measure("24(1)e4cm")
      assert     Measure("26(1)e4cm") >= Measure("24(1)e4cm")
      assert     Measure("27(1)e4cm") >= Measure("24(1)e4cm")
      # Unitless
      assert not Measure("21(1)e4") >= Measure("24(1)e4")
      assert not Measure("22(1)e4") >= Measure("24(1)e4")
      assert not Measure("23(1)e4") >= Measure("24(1)e4")
      assert     Measure("24(1)e4") >= Measure("24(1)e4")
      assert     Measure("25(1)e4") >= Measure("24(1)e4")
      assert     Measure("26(1)e4") >= Measure("24(1)e4")
      assert     Measure("27(1)e4") >= Measure("24(1)e4")
    # UnitExceptions 
    if(True):
      with pytest.raises(IncompatibleUnitException):
        Measure("12 mg") >= Measure("12 uL")
  
  # Addition & Subtraction Operators
  def test_add(self):
    # Measure
    if(True):
      # Values and Certainties
      assert Measure("24(4)cm") + Measure("24(3)cm") == Measure("48(5)cm")
      assert Measure("24(3)cm") + Measure("24(4)cm") == Measure("48(5)cm")
      assert Measure("12(3)cm") + Measure("36(4)cm") == Measure("48(5)cm")
      assert Measure("12(3)")   + Measure("36(4)")   == Measure("48(5)")
      # Zeros
      assert Measure("0cm")     + Measure("36(4)cm") == Measure("36(4)cm")
      assert Measure("36(4)cm") + Measure("0cm")     == Measure("36(4)cm")
      assert Measure("36(4)")   + Measure("0")       == Measure("36(4)")
      # Implied Uncertainty
      assert (Measure("3 cm") + Measure("4 cm")).implied == True
      assert Measure("5 m^2",value="2") + Measure("10m^2") == Measure("20m^2")
      # Preserve Inputs
      a = Measure("12(3)cm")
      b = Measure("36(4)cm")
      c = a+b 
      c = None
      assert a == Measure("12(3)cm")
      assert b == Measure("36(4)cm")
      assert c == None
      # Mixed Units Compatible
      assert Measure("1(0.03)m") + Measure("36(4)cm") == Measure("136(5)cm")
      # Mixed Units Incompatible
      with pytest.raises(IncompatibleUnitException):
        Measure("3 pigs")+Measure("2 sheep")
      with pytest.raises(IncompatibleUnitException):
        Measure("36(4)") + Measure("0cm")
    # Unit
    if(True):
      assert Measure("5 cm")+Unit("cm")   == Measure("6 cm")
      assert Measure("5 cm")+Unit("10cm") == Measure("15 cm")
      with pytest.raises(IncompatibleUnitException):
        Measure("5 cm")+Unit("mg")
    # Number
    if(True):
      # Values and Certainties
      assert          5   + Measure("36(4)") == Measure("41(4)")
      assert         "5"  + Measure("36(4)") == Measure("41(4)")
      assert Decimal("5") + Measure("36(4)") == Measure("41(4)")
      assert Measure("36(4)") +          5   == Measure("41(4)")
      assert Measure("36(4)") +         "5"  == Measure("41(4)")
      assert Measure("36(4)") + Decimal("5") == Measure("41(4)")
      # Zeros
      assert          0   + Measure("36(4)") == Measure("36(4)")
      assert         "0"  + Measure("36(4)") == Measure("36(4)")
      assert Decimal("0") + Measure("36(4)") == Measure("36(4)")
      assert Measure("36(4)") + 0            == Measure("36(4)")
      assert Measure("36(4)") + "0"          == Measure("36(4)")
      assert Measure("36(4)") + Decimal("0") == Measure("36(4)")
      # Implied Uncertainty
      assert (Measure("3") + Decimal("4")).implied == True
      assert (Measure("3") +         "4" ).implied == True
      assert (Measure("3") +          4  ).implied == True
      # Preserve Inputs
      a = Measure("36(4)")
      b = Decimal("5")
      c = a+b 
      c = None
      assert a == Measure("36(4)")
      assert b == Decimal("5")
      assert c == None
      # Error on Non-Unitless Measure + Decimal 
      # Measure + 5
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") + Decimal("5")
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") + "5"
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") + 5
      # 5 + Measure
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Decimal("5") + Measure("36(4)m")
        with pytest.raises(IncompatibleUnitException):
          "5" + Measure("36(4)m")
        with pytest.raises(IncompatibleUnitException):
          5 + Measure("36(4)m")
      
    # String Measures 
    if(True):
      # Values and Certainties
      assert Measure("24(4)cm") + "24(3)cm" == Measure("48(5)cm")
      assert Measure("24(3)cm") + "24(4)cm" == Measure("48(5)cm")
      assert Measure("12(3)cm") + "36(4)cm" == Measure("48(5)cm")
      assert Measure("12(3)")   + "36(4)"   == Measure("48(5)")
      assert "24(4)cm" + Measure("24(3)cm") == Measure("48(5)cm")
      assert "24(3)cm" + Measure("24(4)cm") == Measure("48(5)cm")
      assert "12(3)cm" + Measure("36(4)cm") == Measure("48(5)cm")
      assert "12(3)"   + Measure("36(4)")   == Measure("48(5)")
      # Zeros
      assert Measure("0cm")     + "36(4)cm" == Measure("36(4)cm")
      assert Measure("36(4)cm") + "0cm"     == Measure("36(4)cm")
      assert Measure("36(4)")   + "0"       == Measure("36(4)")
      assert "0cm"     + Measure("36(4)cm") == Measure("36(4)cm")
      assert "36(4)cm" + Measure("0cm")     == Measure("36(4)cm")
      assert "36(4)"   + Measure("0")       == Measure("36(4)")
      # Implied Uncertainty
      assert (Measure("3 cm") + "4 cm").implied == True
      assert ("3 cm" + Measure("4 cm")).implied == True
      assert Measure("5 m^2",value="2") + "10m^2" == Measure("20m^2")
      assert "10m^2" + Measure("5 m^2",value="2") == Measure("20m^2")
      # Preserve Inputs
      a = Measure("12(3)cm")
      b = "36(4)cm"
      c = a+b 
      c = None
      assert a == Measure("12(3)cm")
      assert b == "36(4)cm"
      assert c == None
      # Mixed Units Compatible
      assert Measure("1(0.03)m") + "36(4)cm" == Measure("136(5)cm")
      assert "1(0.03)m" + Measure("36(4)cm") == Measure("136(5)cm")
      # Mixed Units Incompatible
      with pytest.raises(IncompatibleUnitException):
        Measure("3 pigs")+"2 sheep"
      with pytest.raises(IncompatibleUnitException):
        "3 pigs"+Measure("2 sheep")
      with pytest.raises(IncompatibleUnitException):
        Measure("36(4)") + "0cm"
      with pytest.raises(IncompatibleUnitException):
        "36(4)" + Measure("0cm")
  def test_sub(self):
    # Measure
    if(True):
      # Certainty and Values
      assert Measure("24(4)cm") - Measure("24(3)cm") == Measure("0(5)cm")
      assert Measure("24(3)cm") - Measure("24(4)cm") == Measure("0(5)cm")
      assert Measure("12(3)cm") - Measure("36(4)cm") == Measure("-24(5)cm")
      # Zeros
      assert Measure("0cm")     - Measure("36(4)cm") == Measure("-36(4)cm")
      assert Measure("36(4)cm") - Measure("0cm")     == Measure("36(4)cm")
      # Implied Uncertainty
      assert (Measure("3 cm") - Measure("4 cm")).implied == True
      assert Measure("5 m^2",value="2") - Measure("5 m^2") == Measure("5 m^2")
      # Preserve Inputs 
      a = Measure("12(3)cm")
      b = Measure("36(4)cm")
      c = a-b 
      c = None
      assert a == Measure("12(3)cm")
      assert b == Measure("36(4)cm")
      assert c == None
      # Mixed Units Compatible
      assert Measure("1(0.03)m") - Measure("36(4)cm") == Measure("64(5)cm")
      # Mixed Units Incompatible
      with pytest.raises(IncompatibleUnitException):
        Measure("3 pigs") - Measure("2 sheep")
      with pytest.raises(IncompatibleUnitException):
        Measure("36(4)") - Measure("0cm")
    # Number
    if(True):
      # Certainty and Values
      assert Decimal("5") - Measure("36(4)") == Measure("-31(4)")
      assert         "5"  - Measure("36(4)") == Measure("-31(4)")
      assert          5   - Measure("36(4)") == Measure("-31(4)")
      assert Measure("36(4)") - Decimal("5") == Measure("31(4)")
      assert Measure("36(4)") -         "5"  == Measure("31(4)")
      assert Measure("36(4)") -          5   == Measure("31(4)")
      # Zeros
      assert          0   - Measure("36(4)") == Measure("-36(4)")
      assert         "0"  - Measure("36(4)") == Measure("-36(4)")
      assert Decimal("0") - Measure("36(4)") == Measure("-36(4)")
      assert Measure("36(4)") -          0   == Measure("36(4)")
      assert Measure("36(4)") -         "0"  == Measure("36(4)")
      assert Measure("36(4)") - Decimal("0") == Measure("36(4)")
      # Implied Uncertainty
      assert (Measure("3") - Decimal("4")).implied == True
      assert (Measure("3") -         "4" ).implied == True
      assert (Measure("3") -          4  ).implied == True
      # Preserve Inputs 
      a = Measure("36(4)")
      b = Decimal("5")
      c = a-b 
      c = None
      assert a == Measure("36(4)")
      assert b == Decimal("5")
      assert c == None
      # Error on Non-Unitless Measure - Decimal 
      # Measure - 5 
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") - Decimal("5")
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") - "5"
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)m") - 5
      # 5 - Measure
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Decimal("5") - Measure("36(4)m")
        with pytest.raises(IncompatibleUnitException):
          "5" - Measure("36(4)m")
        with pytest.raises(IncompatibleUnitException):
          5 - Measure("36(4)m")
      # Measure - 0
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)cm") - Decimal("0")
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)cm") - "0"
        with pytest.raises(IncompatibleUnitException):
          Measure("36(4)cm") - 0
      # 0 - Measure
      if(True):
        with pytest.raises(IncompatibleUnitException):
          Decimal("0") - Measure("36(4)cm")
        with pytest.raises(IncompatibleUnitException):
          "0" - Measure("36(4)cm")
        with pytest.raises(IncompatibleUnitException):
          0 - Measure("36(4)cm")
    # Unit
    if(True):
      assert Measure("5 cm")-Unit("cm")   == Measure("4 cm")
      assert Measure("5 cm")-Unit("10cm") == Measure("-5 cm")
      with pytest.raises(IncompatibleUnitException):
        Measure("5 cm")-Unit("mg")
    # String Measures 
    if(True):
      # Certainty and Values
      assert Measure("24(4)cm") - "24(3)cm" == Measure("0(5)cm")
      assert Measure("24(3)cm") - "24(4)cm" == Measure("0(5)cm")
      assert Measure("12(3)cm") - "36(4)cm" == Measure("-24(5)cm")
      assert "24(4)cm" - Measure("24(3)cm") == Measure("0(5)cm")
      assert "24(3)cm" - Measure("24(4)cm") == Measure("0(5)cm")
      assert "12(3)cm" - Measure("36(4)cm") == Measure("-24(5)cm")
      # Zeros
      assert Measure("0cm")     - "36(4)cm" == Measure("-36(4)cm")
      assert Measure("36(4)cm") - "0cm"     == Measure("36(4)cm")
      assert "0cm"     - Measure("36(4)cm") == Measure("-36(4)cm")
      assert "36(4)cm" - Measure("0cm")     == Measure("36(4)cm")
      # Implied Uncertainty
      assert (Measure("3 cm") - "4 cm").implied == True
      assert ("3 cm" - Measure("4 cm")).implied == True
      assert Measure("5 m^2",value="2") - "5 m^2" == Measure("5 m^2")
      assert "5 m^2" - Measure("5 m^2",value="2") == Measure("-5 m^2")
      # Preserve Inputs 
      a = Measure("12(3)cm")
      b = Measure("36(4)cm")
      c = a-b 
      c = None
      assert a == Measure("12(3)cm")
      assert b == Measure("36(4)cm")
      assert c == None
      # Mixed Units Compatible
      assert Measure("1(0.03)m") - "36(4)cm" == Measure("64(5)cm")
      assert "1(0.03)m" - Measure("36(4)cm") == Measure("64(5)cm")
      # Mixed Units Incompatible
      with pytest.raises(IncompatibleUnitException):
        Measure("3 pigs") - "2 sheep"
      with pytest.raises(IncompatibleUnitException):
        "3 pigs" - Measure("2 sheep")
      with pytest.raises(IncompatibleUnitException):
        Measure("36(4)") - "0cm"
      with pytest.raises(IncompatibleUnitException):
        "36(4)" - Measure("0cm")
  
  # Multiplication & Division Operators
  # To-Do: "1 * 5 cm" is a measure. "cm" is a Unit Fix this.
  # sig = measure._sqrt_( (1/y)**2 * dx**2 + (-1* y**-2 *x)**2 * dy**2)
  
  def test_measure_measure_add(self):
    def meas_meas_add(
        x=None,dx=None,xu=None, 
        y=None,dy=None,yu=None, 
        u=None,du=None,mu=None,
        v=None,dv=None,mv=None,
        value = None, error=None, unit=None,
        implied=None):
      log.warning(f"x={x} , dx={dx} , xu={xu} , y={y} , dy={dy} , yu={yu}")
      floats = all([isinstance(i,float) or i==None or i==0 for i in [x,dx,y,dy]])
      
      if(floats):
        # Context Settings
        if( u==None):  u = float( x)           # If  x==None, give value
        if(du==None): du = float(dx)           # If dx==None, give value
        if(mu==None): mu = float(xu.magnitude) # If xu==None, give value
        
        if( v==None):  v = float( y)           # If  y==None, give value
        if(dv==None): dv = float(dy)           # If dy==None, give value
        if(mv==None): mv = float(yu.magnitude) # If yu==None, give value
        
        # Standard Div Values
        if(value == None): value = u+v
        if(unit  == None): 
          identical_units = xu.symbols == yu.symbols and xu.magnitude == yu.magnitude
          if(identical_units): unit = xu
          else: unit = xu.decompose()
          
        n  = float( unit.magnitude )
        if(error == None):  error = measure._sqrt_( (du*mu)**2 + (dv*mv)**2 ) / n
        
        # Standard Div Assertions
        assert isinstance(   (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ), Measure )
        assert math.isclose( (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).value , value )
        assert math.isclose( (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).error , error )
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).implied == implied
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).units.symbols   == unit.symbols
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).units.magnitude == unit.magnitude
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ) == Measure(units=unit, value= value, error=error)
      else:
        # Context Settings
        if( u==None):  u = Decimal( x)  # If  x==None, give value
        if(du==None): du = Decimal(dx)  # If dx==None, give value
        if(mu==None): mu = xu.magnitude # If xu==None, give value
        
        if( v==None):  v = Decimal( y)  # If  y==None, give value
        if(dv==None): dv = Decimal(dy)  # If dy==None, give value
        if(mv==None): mv = yu.magnitude # If yu==None, give value
        
        # Standard Div Values
        if(value == None): value = u+v
        if(unit  == None): 
          identical_units = xu.symbols == yu.symbols and xu.magnitude == yu.magnitude
          if(identical_units): unit = xu
          else: unit = xu.decompose()
        n  = unit.magnitude
        if(error == None): error = measure._sqrt_( (du*mu)**2 + (dv*mv)**2 ) / n
        # Standard Div Assertions
        assert isinstance(            (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ), Measure )
        assert Measure._dec_isclose_( (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).value , value )
        assert Measure._dec_isclose_( (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).error , error )
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).implied == implied
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).units.symbols   == unit.symbols
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ).units.magnitude == unit.magnitude
        assert (  Measure(value=x,error=dx,unit=xu)  +  Measure(value=y,error=dy,unit=yu)  ) == Measure(units=unit, value= value, error=error)
    #
    # Measure (Explicit Error) + Measure (Explicit Error) = Measure (Explicit Error)
    if(True):
      # Unitless + Unitless
      if(True):
        # Value 1: Int
        meas_meas_add(
          x=4     , dx=2              , xu=Unit(), 
          y=3     , dy=1              , yu=Unit(), 
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 2: Float
        meas_meas_add(
          x=0.4   , dx=0.2            , xu=Unit(), 
          y=0.3   , dy=0.1            , yu=Unit(), 
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 3: Decimal
        meas_meas_add(
          x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
          y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
          u=None          , du=None           , mu=None,
          v=None          , dv=None           , mv=None,
          implied=False)
        # Value 4: Negative
        meas_meas_add(
          x=-4    , dx=2              , xu=Unit(), 
          y=-3    , dy=1              , yu=Unit(),
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 5: Zero
        if(True):
          # Value 1: Int
          meas_meas_add(
            x=4     , dx=2              , xu=Unit(), 
            y=0     , dy=1              , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_add(
            x=0.4   , dx=0.2            , xu=Unit(), 
            y=0.0   , dy=0.1            , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_add(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
            y=Decimal("0")  , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2) 
          b = Measure(value=3,error=2)
          c = a+b
          c = None
          assert a == Measure(value=4,error=2) 
          assert b == Measure(value=3,error=2)
      # Unitless + Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=4,error=2,unit=Unit()) + Measure(value=3,error=1,unit=Unit("cm"))
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=0.4,error=0.2,unit=Unit()) + Measure(value=0.3,error=0.1,unit=Unit("cm"))
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm"))
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=-4,error=2,unit=Unit()) + Measure(value=-3,error=1,unit=Unit("cm"))
          # Value 5: Zero Value, Something Error
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=4,error=2,unit=Unit()) + Measure(value=0,error=1,unit=Unit("cm"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=2,unit=Unit()) + Measure(value=3,error=1,unit=Unit("cm"))
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.4,error=0.2,unit=Unit()) + Measure(value=0,error=0.1,unit=Unit("cm"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=0.2,unit=Unit()) + Measure(value=0.3,error=0.1,unit=Unit("cm"))
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("cm"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm"))
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-4,error=2,unit=Unit()) + Measure(value=0,error=1,unit=Unit("cm"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=2,unit=Unit()) + Measure(value=-3,error=1,unit=Unit("cm"))
          # Value 5: Zero Value, Zero Error
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=0     , dx=0              , xu=Unit(), 
              y=3     , dy=1              , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=4     , dx=2              , xu=Unit(), 
              y=0     , dy=0              , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0     , dx=0              , xu=Unit(), 
              y=0.3   , dy=0.1            , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=0.4   , dx=0.2            , xu=Unit(), 
              y=0     , dy=0              , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("0")  , dx=Decimal("0")   , xu=Unit(), 
              y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
              y=Decimal("0")  , dy=Decimal("0")   , yu=Unit("cm"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
        # Magnitude Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=4,error=2,unit=Unit()) + Measure(value=3,error=1,unit=Unit("5 m^2"))
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=0.4,error=0.2,unit=Unit()) + Measure(value=0.3,error=0.1,unit=Unit("5 m^2"))
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2"))
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=-4,error=2,unit=Unit()) + Measure(value=-3,error=1,unit=Unit("5 m^2"))
          # Value 5: Zero Value, Something Error
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=4,error=2,unit=Unit()) + Measure(value=0,error=1,unit=Unit("5 m^2"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=2,unit=Unit()) + Measure(value=3,error=1,unit=Unit("5 m^2"))
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.4,error=0.2,unit=Unit()) + Measure(value=0,error=0.1,unit=Unit("5 m^2"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=0.2,unit=Unit()) + Measure(value=0.3,error=0.1,unit=Unit("5 m^2"))
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("5 m^2"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit()) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2"))
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-4,error=2,unit=Unit()) + Measure(value=0,error=1,unit=Unit("5 m^2"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=2,unit=Unit()) + Measure(value=-3,error=1,unit=Unit("5 m^2"))
          # Value 5: Zero Value, Zero Error
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=0     , dx=0              , xu=Unit(), 
              y=3     , dy=1              , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=4     , dx=2              , xu=Unit(), 
              y=0     , dy=0              , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0     , dx=0              , xu=Unit(), 
              y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=0.4   , dx=0.2            , xu=Unit(), 
              y=0     , dy=0              , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("0")  , dx=Decimal("0")   , xu=Unit(), 
              y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
              y=Decimal("0")  , dy=Decimal("0")   , yu=Unit("5 m^2"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
        # Convoluted Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=300,error=2,unit=Unit()) + Measure(value=27,error=1,unit=Unit("\u00B0C"))
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=299.9,error=0.02,unit=Unit()) + Measure(value=26.85,error=0.01,unit=Unit("\u00B0C"))
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit()) + Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=300,error=2,unit=Unit()) + Measure(value=-27,error=1,unit=Unit("\u00B0C"))
          # Value 5: Zero Value, Something Error
          if(True):
            # Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=300,error=2,unit=Unit()) + Measure(value=0,error=1,unit=Unit("\u00B0C"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=2,unit=Unit()) + Measure(value=27,error=1,unit=Unit("\u00B0C"))
            # Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=300.0,error=0.02,unit=Unit()) + Measure(value=0.0,error=0.01,unit=Unit("\u00B0C"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.0,error=0.02,unit=Unit()) + Measure(value=26.85,error=0.01,unit=Unit("\u00B0C"))
            # Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit()) + Measure(value=Decimal("0"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("0.02"),unit=Unit()) + Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
          # Value 5: Zero Value, Zero Error
          if(True):
            # Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=300,error=2,unit=Unit()) + Measure(value=0,error=0,unit=Unit("\u00B0C"))
            meas_meas_add(
              x=0             , dx=0              , xu=Unit(), 
              y=27            , dy=1              , yu=Unit("\u00B0C"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("\u00B0C"),
              implied=False)
            # Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=300.0,error=0.02,unit=Unit()) + Measure(value=0.0,error=0.0,unit=Unit("\u00B0C"))
            meas_meas_add(
              x=0             , dx=0              , xu=Unit(), 
              y=26.85         , dy=0.01           , yu=Unit("\u00B0C"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("\u00B0C"),
              implied=False)
            # Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit()) + Measure(value=Decimal("0"),error=Decimal("0"),unit=Unit("\u00B0C"))
            meas_meas_add(
              x=Decimal("0")      , dx=Decimal("0")     , xu=Unit(), 
              y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
              u=None              , du=None             , mu=None,
              v=None              , dv=None             , mv=None,
              unit=Unit("\u00B0C"), 
              implied=False)
      # Unit + Unitless
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=3,error=1,unit=Unit("cm")) + Measure(value=4,error=2,unit=Unit())
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=0.3,error=0.1,unit=Unit("cm")) + Measure(value=0.4,error=0.2,unit=Unit())
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm")) + Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit())
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=-3,error=1,unit=Unit("cm")) + Measure(value=-4,error=2,unit=Unit())
          # Value 5: Zero Value, Something Error
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=1,unit=Unit("cm")) + Measure(value=4,error=2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=3,error=1,unit=Unit("cm")) + Measure(value=0,error=2,unit=Unit())
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=0.1,unit=Unit("cm")) + Measure(value=0.4,error=0.2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.3,error=0.1,unit=Unit("cm")) + Measure(value=0,error=0.2,unit=Unit())
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("cm")) + Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm")) + Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit())
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=1,unit=Unit("cm")) + Measure(value=-4,error=2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-3,error=1,unit=Unit("cm")) + Measure(value=0,error=2,unit=Unit())
          # Value 5: Zero Value, Zero Error
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=3     , dx=1              , xu=Unit("cm"), 
              y=0     , dy=0              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=0     , dx=0              , xu=Unit("cm"), 
              y=4     , dy=2              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0.3   , dx=0.1            , xu=Unit("cm"), 
              y=0     , dy=0              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=0     , dx=0              , xu=Unit("cm"), 
              y=0.4   , dy=0.2            , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("30") , dx=Decimal("10")  , xu=Unit("cm"), 
              y=Decimal("0")  , dy=Decimal("0")   , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("cm"),
              implied=False)
            meas_meas_add(
              x=Decimal("0")  , dx=Decimal("0")   , xu=Unit("cm"), 
              y=Decimal("40") , dy=Decimal("20")  , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
        # Magnitude Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=3,error=1,unit=Unit("5 m^2")) + Measure(value=4,error=2,unit=Unit())
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=0.3,error=0.1,unit=Unit("5 m^2")) + Measure(value=0.4,error=0.2,unit=Unit())
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2")) + Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit())
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=-3,error=1,unit=Unit("5 m^2")) + Measure(value=-4,error=2,unit=Unit())
          # Value 5: Zero Value, Something Error
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=1,unit=Unit("5 m^2")) + Measure(value=4,error=2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=3,error=1,unit=Unit("5 m^2")) + Measure(value=0,error=2,unit=Unit())
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=0.1,unit=Unit("5 m^2")) + Measure(value=0.4,error=0.2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.3,error=0.1,unit=Unit("5 m^2")) + Measure(value=0,error=0.2,unit=Unit())
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("5 m^2")) + Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2")) + Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit())
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=1,unit=Unit("5 m^2")) + Measure(value=-4,error=2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-3,error=1,unit=Unit("5 m^2")) + Measure(value=0,error=2,unit=Unit())
          # Value 5: Zero Value, Zero Error
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=3     , dx=1              , xu=Unit("5 m^2"), 
              y=0     , dy=0              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=0     , dx=0              , xu=Unit("5 m^2"), 
              y=4     , dy=2              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0.3   , dx=0.1            , xu=Unit("5 m^2"), 
              y=0     , dy=0              , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=0     , dx=0              , xu=Unit("5 m^2"), 
              y=0.4   , dy=0.2            , yu=Unit(), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("30") , dx=Decimal("10")  , xu=Unit("5 m^2"), 
              y=Decimal("0")  , dy=Decimal("0")   , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("5 m^2"),
              implied=False)
            meas_meas_add(
              x=Decimal("0")  , dx=Decimal("0")   , xu=Unit("5 m^2"), 
              y=Decimal("40") , dy=Decimal("20")  , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit(),
              implied=False)
        # Convoluted Units
        if(True):
          # Value 1: Int
          with pytest.raises(IncompatibleUnitException):
            Measure(value=27,error=1,unit=Unit("\u00B0C")) + Measure(value=300,error=2,unit=Unit())
          # Value 2: Float
          with pytest.raises(IncompatibleUnitException):
            Measure(value=26.85,error=0.01,unit=Unit("\u00B0C")) + Measure(value=299.9,error=0.02,unit=Unit())
          # Value 3: Decimal
          with pytest.raises(IncompatibleUnitException):
            Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C")) + Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit())
          # Value 4: Negative
          with pytest.raises(IncompatibleUnitException):
            Measure(value=-27,error=1,unit=Unit("\u00B0C")) + Measure(value=300,error=2,unit=Unit())
          # Value 5: Zero Value, Something Error
          if(True):
            # Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=1,unit=Unit("\u00B0C")) + Measure(value=300,error=2,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=27,error=1,unit=Unit("\u00B0C")) + Measure(value=0,error=2,unit=Unit())
            # Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.0,error=0.01,unit=Unit("\u00B0C")) + Measure(value=300.0,error=0.02,unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=26.85,error=0.01,unit=Unit("\u00B0C")) + Measure(value=0.0,error=0.02,unit=Unit())
            # Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("0.01"),unit=Unit("\u00B0C")) + Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit())
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C")) + Measure(value=Decimal("0"),error=Decimal("0.02"),unit=Unit())
          # Value 5: Zero Value, Zero Error
          if(True):
            # Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0,error=0,unit=Unit("\u00B0C")) + Measure(value=300,error=2,unit=Unit())
            meas_meas_add(
              x=27            , dx=1              , xu=Unit("\u00B0C"), 
              y=0             , dy=0              , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("\u00B0C"),
              implied=False)
            # Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.0,error=0.0,unit=Unit("\u00B0C")) + Measure(value=300.0,error=0.02,unit=Unit())
            meas_meas_add(
              x=26.85         , dx=0.01           , xu=Unit("\u00B0C"), 
              y=0             , dy=0              , yu=Unit(), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              unit=Unit("\u00B0C"),
              implied=False)
            # Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("0"),error=Decimal("0"),unit=Unit("\u00B0C")) + Measure(value=Decimal("300"),error=Decimal("0.02"),unit=Unit())
            meas_meas_add(
              x=Decimal("26.85")  , dx=Decimal("0.01")  , xu=Unit("\u00B0C"), 
              y=Decimal("0")      , dy=Decimal("0")     , yu=Unit(), 
              u=None              , du=None             , mu=None,
              v=None              , dv=None             , mv=None,
              unit=Unit("\u00B0C"), 
              implied=False)
      # Unit + Unit
      if(True):
        # Same Units
        if(True):
          # Normal Units
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=4     , dx=2              , xu=Unit("cm"), 
              y=3     , dy=1              , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0.4   , dx=0.2            , xu=Unit("cm"), 
              y=0.3   , dy=0.1            , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
              y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              implied=False)
            # Value 4: Negative
            meas_meas_add(
              x=-4    , dx=2              , xu=Unit("cm"), 
              y=-3    , dy=1              , yu=Unit("cm"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 5: Zero
            if(True):
              # Value 1: Int
              meas_meas_add(
                x=0     , dx=2              , xu=Unit("cm"), 
                y=3     , dy=1              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=4     , dx=2              , xu=Unit("cm"), 
                y=0     , dy=1              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              # Value 2: Float
              meas_meas_add(
                x=0.0   , dx=0.2            , xu=Unit("cm"), 
                y=0.3   , dy=0.1            , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=0.4   , dx=0.2            , xu=Unit("cm"), 
                y=0.0   , dy=0.1            , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              # Value 3: Decimal
              meas_meas_add(
                x=Decimal("0")  , dx=Decimal("20")  , xu=Unit("cm"), 
                y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
                y=Decimal("0")  , dy=Decimal("10")  , yu=Unit("cm"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                implied=False)
              # Value 4: Negative
              meas_meas_add(
                x=0     , dx=2              , xu=Unit("cm"), 
                y=-3    , dy=1              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=-4    , dx=2              , xu=Unit("cm"), 
                y=0     , dy=1              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
          # Magnitude Units
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=4     , dx=2              , xu=Unit("5 m^2"), 
              y=3     , dy=1              , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=0.4   , dx=0.2            , xu=Unit("5 m^2"), 
              y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("40") , dx=Decimal("20")  , xu=Unit("5 m^2"), 
              y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
              u=None          , du=None           , mu=None,
              v=None          , dv=None           , mv=None,
              implied=False)
            # Value 4: Negative
            meas_meas_add(
              x=-4    , dx=2              , xu=Unit("5 m^2"), 
              y=-3    , dy=1              , yu=Unit("5 m^2"), 
              u=None  , du=None           , mu=None,
              v=None  , dv=None           , mv=None,
              implied=False)
            # Value 5: Zero
            if(True):
              # Value 1: Int
              meas_meas_add(
                x=0     , dx=2              , xu=Unit("5 m^2"), 
                y=3     , dy=1              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=4     , dx=2              , xu=Unit("5 m^2"), 
                y=0     , dy=1              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              # Value 2: Float
              meas_meas_add(
                x=0.0   , dx=0.2            , xu=Unit("5 m^2"), 
                y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=0.4   , dx=0.2            , xu=Unit("5 m^2"), 
                y=0.0   , dy=0.1            , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              # Value 3: Decimal
              meas_meas_add(
                x=Decimal("0")  , dx=Decimal("20")  , xu=Unit("5 m^2"), 
                y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=Decimal("40") , dx=Decimal("20")  , xu=Unit("5 m^2"), 
                y=Decimal("0")  , dy=Decimal("10")  , yu=Unit("5 m^2"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                implied=False)
              # Value 4: Negative
              meas_meas_add(
                x=0     , dx=2              , xu=Unit("5 m^2"), 
                y=-3    , dy=1              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
              meas_meas_add(
                x=-4    , dx=2              , xu=Unit("5 m^2"), 
                y=0     , dy=1              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                implied=False)
          # Convoluted Units
          if(True):
            # Value 1: Int
            meas_meas_add(
              x=26                , dx=2    , xu=Unit("\u00B0C"), 
              y=27                , dy=1    , yu=Unit("\u00B0C"), 
              u=Decimal("299.85") , du=None , mu=None,
              v=Decimal("300.15") , dv=None , mv=None,
              value = Decimal("299.85") + Decimal("300.15") - Decimal("273.85"),
              implied=False)
            # Value 2: Float
            meas_meas_add(
              x=26.85 , dx=0.02 , xu=Unit("\u00B0C"), 
              y=26.85 , dy=0.01 , yu=Unit("\u00B0C"), 
              u=300.0 , du=None , mu=None,
              v=300.0 , dv=None , mv=None,
              value = 300.0 + 300.0 - 273.15,
              implied=False)
            # Value 3: Decimal
            meas_meas_add(
              x=Decimal("26.85")  , dx=Decimal("0.02")  , xu=Unit("\u00B0C"), 
              y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
              u=Decimal("300")    , du=None             , mu=None,
              v=Decimal("300")    , dv=None             , mv=None,
              value = Decimal("300") + Decimal("300") - Decimal("273.15"),
              implied=False)
            # Value 4: Negative
            meas_meas_add(
              x=-31               , dx=2    , xu=Unit("\u00B0C"), 
              y=-27               , dy=1    , yu=Unit("\u00B0C"), 
              u=Decimal("242.15") , du=None , mu=None,
              v=Decimal("246.15") , dv=None , mv=None,
              value = Decimal("242.15") + Decimal("246.15") - Decimal("273.15"),
              implied=False)
            # Value 5: Zero
            if(True):
              # Int
              meas_meas_add(
                x=27                , dx=2    , xu=Unit("\u00B0C"), 
                y=0                 , dy=1    , yu=Unit("\u00B0C"), 
                u=Decimal("300.15") , du=None , mu=None,
                v=Decimal("273.15") , dv=None , mv=None,
                value = Decimal("300.15") + Decimal("273.15") - Decimal("273.15"),
                implied=False)
              # Float
              meas_meas_add(
                x=26.85   , dx=0.02 , xu=Unit("\u00B0C"), 
                y=0.0     , dy=0.01 , yu=Unit("\u00B0C"), 
                u=300.0   , du=None , mu=None,
                v=273.15  , dv=None , mv=None,
                value = 300.0+273.15-273.15,
                implied=False)
              # Decimal
              meas_meas_add(
                x=Decimal("26.85")  , dx=Decimal("0.02"), xu=Unit("\u00B0C"), 
                y=Decimal("0")      , dy=Decimal("0.01"), yu=Unit("\u00B0C"), 
                u=Decimal("300")    , du=None           , mu=None,
                v=Decimal("273.15") , dv=None           , mv=None,
                value = Decimal("300") + Decimal("273.15") - Decimal("273.15"),
                implied=False)
        # Different Units
        if(True):
          # Normal Units
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=4,error=2,unit=Unit("s")) + Measure(value=3,error=1,unit=Unit("cm"))
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.4,error=0.2,unit=Unit("s")) + Measure(value=0.3,error=0.1,unit=Unit("cm"))
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit("s")) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm"))
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-4,error=2,unit=Unit("s")) + Measure(value=-3,error=1,unit=Unit("cm"))
            # Value 5: Zero Value, Something Error
            if(True):
              # Value 1: Int
              with pytest.raises(IncompatibleUnitException):
                Measure(value=4,error=2,unit=Unit("s")) + Measure(value=0,error=1,unit=Unit("cm"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=2,unit=Unit("s")) + Measure(value=3,error=1,unit=Unit("cm"))
              # Value 2: Float
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0.4,error=0.2,unit=Unit("s")) + Measure(value=0,error=0.1,unit=Unit("cm"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=0.2,unit=Unit("s")) + Measure(value=0.3,error=0.1,unit=Unit("cm"))
              # Value 3: Decimal
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit("s")) + Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("cm"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit("s")) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("cm"))
              # Value 4: Negative
              with pytest.raises(IncompatibleUnitException):
                Measure(value=-4,error=2,unit=Unit("s")) + Measure(value=0,error=1,unit=Unit("cm"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=2,unit=Unit("s")) + Measure(value=-3,error=1,unit=Unit("cm"))
            # Value 5: Zero Value, Zero Error
            if(True):
              # Value 1: Int
              meas_meas_add(
                x=0     , dx=0              , xu=Unit("s"), 
                y=3     , dy=1              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("cm"),
                implied=False)
              meas_meas_add(
                x=4     , dx=2              , xu=Unit("s"), 
                y=0     , dy=0              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("s"),
                implied=False)
              # Value 2: Float
              meas_meas_add(
                x=0     , dx=0              , xu=Unit("s"), 
                y=0.3   , dy=0.1            , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("cm"),
                implied=False)
              meas_meas_add(
                x=0.4   , dx=0.2            , xu=Unit("s"), 
                y=0     , dy=0              , yu=Unit("cm"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("s"),
                implied=False)
              # Value 3: Decimal
              meas_meas_add(
                x=Decimal("0")  , dx=Decimal("0")   , xu=Unit("s"), 
                y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                unit=Unit("cm"),
                implied=False)
              meas_meas_add(
                x=Decimal("40") , dx=Decimal("20")  , xu=Unit("s"), 
                y=Decimal("0")  , dy=Decimal("0")   , yu=Unit("cm"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                unit=Unit("s"),
                implied=False)
          # Magnitude Units
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=4,error=2,unit=Unit("5 s")) + Measure(value=3,error=1,unit=Unit("5 m^2"))
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=0.4,error=0.2,unit=Unit("5 s")) + Measure(value=0.3,error=0.1,unit=Unit("5 m^2"))
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit("5 s")) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2"))
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=-4,error=2,unit=Unit("5 s")) + Measure(value=-3,error=1,unit=Unit("5 m^2"))
            # Value 5: Zero Value, Something Error
            if(True):
              # Value 1: Int
              with pytest.raises(IncompatibleUnitException):
                Measure(value=4,error=2,unit=Unit("5 s")) + Measure(value=0,error=1,unit=Unit("5 m^2"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=2,unit=Unit("5 s")) + Measure(value=3,error=1,unit=Unit("5 m^2"))
              # Value 2: Float
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0.4,error=0.2,unit=Unit("5 s")) + Measure(value=0,error=0.1,unit=Unit("5 m^2"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=0.2,unit=Unit("5 s")) + Measure(value=0.3,error=0.1,unit=Unit("5 m^2"))
              # Value 3: Decimal
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("40"),error=Decimal("20"),unit=Unit("5 s")) + Measure(value=Decimal("0"),error=Decimal("10"),unit=Unit("5 m^2"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("0"),error=Decimal("20"),unit=Unit("5 s")) + Measure(value=Decimal("30"),error=Decimal("10"),unit=Unit("5 m^2"))
              # Value 4: Negative
              with pytest.raises(IncompatibleUnitException):
                Measure(value=-4,error=2,unit=Unit("5 s")) + Measure(value=0,error=1,unit=Unit("5 m^2"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=2,unit=Unit("5 s")) + Measure(value=-3,error=1,unit=Unit("5 m^2"))
            # Value 5: Zero Value, Zero Error
            if(True):
              # Value 1: Int
              meas_meas_add(
                x=0     , dx=0              , xu=Unit("5 s"), 
                y=3     , dy=1              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("5 m^2"),
                implied=False)
              meas_meas_add(
                x=4     , dx=2              , xu=Unit("5 s"), 
                y=0     , dy=0              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("5 s"),
                implied=False)
              # Value 2: Float
              meas_meas_add(
                x=0     , dx=0              , xu=Unit("5 s"), 
                y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("5 m^2"),
                implied=False)
              meas_meas_add(
                x=0.4   , dx=0.2            , xu=Unit("5 s"), 
                y=0     , dy=0              , yu=Unit("5 m^2"), 
                u=None  , du=None           , mu=None,
                v=None  , dv=None           , mv=None,
                unit=Unit("5 s"),
                implied=False)
              # Value 3: Decimal
              meas_meas_add(
                x=Decimal("0")  , dx=Decimal("0")   , xu=Unit("5 s"), 
                y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                unit=Unit("5 m^2"),
                implied=False)
              meas_meas_add(
                x=Decimal("40") , dx=Decimal("20")  , xu=Unit("5 s"), 
                y=Decimal("0")  , dy=Decimal("0")   , yu=Unit("5 m^2"), 
                u=None          , du=None           , mu=None,
                v=None          , dv=None           , mv=None,
                unit=Unit("5 s"),
                implied=False)
          # Convoluted Units
          if(True):
            # Value 1: Int
            with pytest.raises(IncompatibleUnitException):
              Measure(value=3,error=2,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=27,error=1,unit=Unit("\u00B0C"))
            # Value 2: Float
            with pytest.raises(IncompatibleUnitException):
              Measure(value=2.9,error=0.02,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=26.85,error=0.01,unit=Unit("\u00B0C"))
            # Value 3: Decimal
            with pytest.raises(IncompatibleUnitException):
              Measure(value=Decimal("3"),error=Decimal("0.02"),unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
            # Value 4: Negative
            with pytest.raises(IncompatibleUnitException):
              Measure(value=3,error=2,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=-27,error=1,unit=Unit("\u00B0C"))
            # Value 5: Zero Value, Something Error
            if(True):
              # Int
              with pytest.raises(IncompatibleUnitException):
                Measure(value=3,error=2,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=0,error=1,unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=2,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=27,error=1,unit=Unit("\u00B0C"))
              # Float
              with pytest.raises(IncompatibleUnitException):
                Measure(value=3.0,error=0.02,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=0.0,error=0.01,unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0.0,error=0.02,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=26.85,error=0.01,unit=Unit("\u00B0C"))
              # Decimal
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("3"),error=Decimal("0.02"),unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=Decimal("0"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("0"),error=Decimal("0.02"),unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=Decimal("26.85"),error=Decimal("0.01"),unit=Unit("\u00B0C"))
            # Value 5: Zero Value, Zero Error
            if(True):
              # Int
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=0,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=0,error=0,unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0,error=0,unit=Unit("\u00B0C")) + Measure(value=0,error=0,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS)
              # Float
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0.0,error=0.0,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=0.0,error=0.0,unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=0.0,error=0.0,unit=Unit("\u00B0C")) + Measure(value=0.0,error=0.0,unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS)
              # Decimal
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("0"),error=Decimal("0.0"),unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS) + Measure(value=Decimal("0"),error=Decimal("0"),unit=Unit("\u00B0C"))
              with pytest.raises(IncompatibleUnitException):
                Measure(value=Decimal("0"),error=Decimal("0"),unit=Unit("\u00B0C")) + Measure(value=Decimal("0"),error=Decimal("0.0"),unit=Unit("pH"),definitions=Unit.CONCENTRATION_UNITS)
    # Measure (Explicit Error) + Measure (Implicit Error) = Measure (Implicit Error)
    if(True):
      # Unitless + Unitless
      if(True):
        # Value 1: Int
        meas_meas_add(
          x=4     , dx=None           , xu=Unit(), 
          y=3     , dy=1              , yu=Unit(), 
          u=None  , du=Decimal("0.5") , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 2: Float
        meas_meas_add(
          x=0.4   , dx=None           , xu=Unit(), 
          y=0.3   , dy=0.1            , yu=Unit(), 
          u=None  , du=0.05           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 3: Decimal
        meas_meas_add(
          x=Decimal("40") , dx=None           , xu=Unit(), 
          y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
          u=None          , du=Decimal("5")   , mu=None,
          v=None          , dv=None           , mv=None,
          implied=True)
        # Value 4: Negative
        meas_meas_add(
          x=-4    , dx=None           , xu=Unit(), 
          y=-3    , dy=1              , yu=Unit(),
          u=None  , du=Decimal("0.5") , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 5: Zero
        if(True):
          # Value 1: Int
          meas_meas_add(
            x=4     , dx=None           , xu=Unit(), 
            y=0     , dy=1              , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_add(
            x=0.4   , dx=None           , xu=Unit(), 
            y=0.0   , dy=0.1            , yu=Unit(), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_add(
            x=Decimal("40") , dx=None           , xu=Unit(), 
            y=Decimal("0")  , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None) 
          b = Measure(value=3,error=2)
          c = a+b
          c = None
          assert a == Measure(value=4,error=None) 
          assert b == Measure(value=3,error=2)
    
    
    
  
  def test_measure_measure_div(self):
    
    assert False
    
    def meas_meas_div(
        x=None,dx=None,xu=None, 
        y=None,dy=None,yu=None, 
        u=None,du=None,mu=None,
        v=None,dv=None,mv=None,
        value = None, error=None, unit=None,
        implied=None):
      log.warning(f"x={x} , dx={dx} , xu={xu} , y={y} , dy={dy} , yu={yu}")
      floats = all([isinstance(i,float) or i==None for i in [x,dx,y,dy]])
      
      if(floats):
        # Context Settings
        if( u==None):  u = float( x)           # If  x==None, give value
        if(du==None): du = float(dx)           # If dx==None, give value
        if(mu==None): mu = float(xu.magnitude) # If xu==None, give value
        
        if( v==None):  v = float( y)           # If  y==None, give value
        if(dv==None): dv = float(dy)           # If dy==None, give value
        if(mv==None): mv = float(yu.magnitude) # If yu==None, give value
        
        # Standard Div Values
        if(value == None): value = u/v
        if(unit  == None): unit  = xu/yu
        n  = float( (xu/yu).magnitude )
        if(error == None):  error = measure._sqrt_( (1/(v*mv))**2 * (du*mu)**2 + (-1 * (v*mv) **-2 * (u*mu) )**2 * (dv*mv) **2) / n
        # Standard Div Assertions
        assert isinstance( ( Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ), Measure )
        assert math.isclose( (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).value , value )
        assert math.isclose( (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).error , error )
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).implied == implied
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).units.symbols   == unit.symbols
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).units.magnitude == unit.magnitude
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ) == Measure(units=unit, value= value, error=error)
      else:
        # Context Settings
        if( u==None):  u = Decimal( x)  # If  x==None, give value
        if(du==None): du = Decimal(dx)  # If dx==None, give value
        if(mu==None): mu = xu.magnitude # If xu==None, give value
        
        if( v==None):  v = Decimal( y)  # If  y==None, give value
        if(dv==None): dv = Decimal(dy)  # If dy==None, give value
        if(mv==None): mv = yu.magnitude # If yu==None, give value
        
        # Standard Div Values
        if(value == None): value = u/v
        if(unit  == None): unit  = xu/yu
        n  = (xu/yu).magnitude
        if(error == None): error = measure._sqrt_( (1/(v*mv))**2 * (du*mu)**2 + (-1 * (v*mv) **-2 * (u*mu) )**2 * (dv*mv) **2) / n
        # Standard Div Assertions
        assert isinstance( ( Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ), Measure )
        assert Measure._dec_isclose_( (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).value , value )
        assert Measure._dec_isclose_( (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).error , error )
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).implied == implied
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).units.symbols   == unit.symbols
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ).units.magnitude == unit.magnitude
        assert (  Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)  ) == Measure(units=unit, value= value, error=error)
    
    # Measure (Explicit Error) / Measure (Explicit Error) = Measure (Explicit Error)
    if(True):
      # Unitless / Unitless
      if(True):
        # Value 1: Int
        meas_meas_div(
          x=4     , dx=2              , xu=Unit(), 
          y=3     , dy=1              , yu=Unit(), 
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 2: Float
        meas_meas_div(
          x=0.4   , dx=0.2            , xu=Unit(), 
          y=0.3   , dy=0.1            , yu=Unit(), 
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 3: Decimal
        meas_meas_div(
          x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
          y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
          u=None          , du=None           , mu=None,
          v=None          , dv=None           , mv=None,
          implied=False)
        # Value 4: Negative
        meas_meas_div(
          x=-4    , dx=2              , xu=Unit(), 
          y=-3    , dy=1              , yu=Unit(),
          u=None  , du=None           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=False)
        # Value 5: Zero
        if(True):
          # Int
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 4,2,Unit()
            y,dy,yu = 0,1,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Float
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 0.4,0.2,Unit()
            y,dy,yu = 0.0,0.1,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Decimal 
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
            y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2) 
          b = Measure(value=3,error=2)
          c = a/b
          c = None
          assert a == Measure(value=4,error=2) 
          assert b == Measure(value=3,error=2)
      # Unitless / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit(), 
            y=3     , dy=1              , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit(), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit(), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit()
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit()
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit(), 
            y=3     , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit(), 
            y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit(), 
            y=-3    , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit()
              y,dy,yu = 0,1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit()
              y,dy,yu = 0.0,0.1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=2    , xu=Unit(), 
            y=27                , dy=1    , yu=Unit("\u00B0C"), 
            u=None              , du=None , mu=None,
            v=Decimal("300.15") , dv=None , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=299.9 , dx=0.02 , xu=Unit(), 
            y=26.85 , dy=0.01 , yu=Unit("\u00B0C"), 
            u=None  , du=None , mu=None,
            v=300.0 , dv=None , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=Decimal("0.02")  , xu=Unit(), 
            y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
            u=None              , du=None             , mu=None,
            v=Decimal("300")    , dv=None             , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=300               , dx=2    , xu=Unit(), 
            y=-27               , dy=1    , yu=Unit("\u00B0C"), 
            u=None              , du=None , mu=None,
            v=Decimal("246.15") , dv=None , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=300               , dx=2    , xu=Unit(), 
              y=0                 , dy=1    , yu=Unit("\u00B0C"), 
              u=None              , du=None , mu=None,
              v=Decimal("273.15") , dv=None , mv=None,
              implied=False)
            # Float
            meas_meas_div(
              x=300.0   , dx=0.02 , xu=Unit(), 
              y=0.0     , dy=0.01 , yu=Unit("\u00B0C"), 
              u=None    , du=None , mu=None,
              v=273.15  , dv=None , mv=None,
              implied=False)
            # Decimal
            meas_meas_div(
              x=Decimal("300")    , dx=Decimal("0.02")  , xu=Unit(), 
              y=Decimal("0")      , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
              u=None              , du=None             , mu=None,
              v=Decimal("273.15") , dv=None             , mv=None,
              implied=False)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2) 
          b = Measure(value=3,error=2,unit=Unit("cm"))
          c = a/b
          c = None
          assert a == Measure(value=4,error=2) 
          assert b == Measure(value=3,error=2,unit=Unit("cm"))
      # Unit / Unitless
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit("cm"), 
            y=3     , dy=1              , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit("cm"), 
            y=0.3   , dy=0.1            , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit("cm"), 
            y=-3    , dy=1              , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("cm")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("cm")
              y,dy,yu = 0.0,0.1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("cm")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit("5 m^2"), 
            y=3     , dy=1              , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit("5 m^2"), 
            y=0.3   , dy=0.1            , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("5 m^2"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit("5 m^2"), 
            y=-3    , dy=1              , yu=Unit(), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("5 m^2")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("5 m^2")
              y,dy,yu = 0.0,0.1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("5 m^2")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=27                , dx=1    , xu=Unit("\u00B0C"), 
            y=300               , dy=2    , yu=Unit(), 
            u=Decimal("300.15") , du=None , mu=None,
            v=None              , dv=None , mv=None,
            value = Decimal("300.15")/Decimal("300") - Decimal("273.15"),
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=26.85 , dx=0.01 , xu=Unit("\u00B0C"), 
            y=299.9 , dy=0.02 , yu=Unit(), 
            u=300.0 , du=None , mu=None,
            v=None  , dv=None , mv=None,
            value  = 300.0/299.9-273.15,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("26.85")  , dx=Decimal("0.01")  , xu=Unit("\u00B0C"), 
            y=Decimal("300")    , dy=Decimal("0.02")  , yu=Unit(), 
            u=Decimal("300")    , du=None             , mu=None,
            v=None              , dv=None             , mv=None,
            value = 1+Decimal("-273.15"),
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-27               , dx=1    , xu=Unit("\u00B0C"), 
            y=300               , dy=2    , yu=Unit(), 
            u=Decimal("246.15") , du=None , mu=None,
            v=None              , dv=None , mv=None,
            value = Decimal("246.15")/Decimal("300") - Decimal("273.15"),
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 27,2,Unit("\u00B0C")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 26.15,0.02,Unit("\u00B0C")
              y,dy,yu = 0.0,0.01,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("26.15"),Decimal("0.02"),Unit("\u00B0C")
              y,dy,yu = Decimal(0),Decimal("0.01"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2,unit=Unit("cm")) 
          b = Measure(value=3,error=2)
          c = a/b
          c = None
          assert a == Measure(value=4,error=2,unit=Unit("cm")) 
          assert b == Measure(value=3,error=2)
      # Unit / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit("s"), 
            y=3     , dy=1              , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit("s"), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("s"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit("s"), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("s")
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("s")
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("s")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit("2 s"), 
            y=3     , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit("2 s"), 
            y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("2 s"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit("2 s"), 
            y=-3    , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("2 s")
              y,dy,yu = 0,1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("2 s")
              y,dy,yu = 0.0,0.1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("2 s")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=2    , xu=Unit("s"), 
            y=27                , dy=1    , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=None , mu=None,
            v=Decimal("300.15") , dv=None , mv=None,
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=300.0 , dx=0.02 , xu=Unit("s"), 
            y=26.85 , dy=0.01 , yu=Unit("\u00B0C"), 
            u=300.0 , du=None , mu=None,
            v=300.0 , dv=None , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=Decimal("0.02")  , xu=Unit("s"), 
            y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=None             , mu=None,
            v=Decimal("300")    , dv=None             , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-31               , dx=2    , xu=Unit("m"), 
            y=-27               , dy=1    , yu=Unit("\u00B0C"), 
            u=Decimal("-31")    , du=None , mu=None,
            v=Decimal("246.15") , dv=None , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=27                , dx=2    , xu=Unit("\u00B0C"), 
              y=0                 , dy=1    , yu=Unit("\u00B0C"), 
              u=Decimal("300.15") , du=None , mu=None,
              v=Decimal("273.15") , dv=None , mv=None,
              implied=False)
            # Float
            meas_meas_div(
              x=26.85   , dx=0.02 , xu=Unit("\u00B0C"), 
              y= 0.0    , dy=0.01 , yu=Unit("\u00B0C"), 
              u=300.0   , du=None , mu=None,
              v=273.15  , dv=None , mv=None,
              implied=False)
            # Decimal
            meas_meas_div(
              x=Decimal("26.85")  , dx=Decimal("0.02"), xu=Unit("\u00B0C"), 
              y=Decimal("0")      , dy=Decimal("0.01"), yu=Unit("\u00B0C"), 
              u=Decimal("300")    , du=None           , mu=None,
              v=Decimal("273.15") , dv=None           , mv=None,
              implied=False)
        # Canceling Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=2              , xu=Unit("cm"), 
            y=3     , dy=1              , yu=Unit("cm"),
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None, 
            implied=False)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=0.2            , xu=Unit("cm"), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=None           , mv=None,
            implied=False)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=2              , xu=Unit("cm"), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=None           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=False)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("cm")
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("cm")
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("cm")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
    # Measure (Explicit Error) / Measure (Implicit Error) = Measure (Implicit Error)
    if(True):
      # Unitless / Unitless
      if(True):
        # Value 1: Int
        meas_meas_div(
          x=4    , dx=2              , xu=Unit(), 
          y=3    , dy=None           , yu=Unit(), 
          u=None , du=None           , mu=None,
          v=None , dv=Decimal('0.5') , mv=None,
          implied=True)
        # Value 2: Float
        meas_meas_div(
          x=0.4  , dx=0.2  , xu=Unit(), 
          y=0.3  , dy=None , yu=Unit(), 
          u=None , du=None , mu=None,
          v=None , dv=0.05 , mv=None,
          implied=True)
        # Value 3: Decimal
        meas_meas_div(
          x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
          y=Decimal("30") , dy=None           , yu=Unit(), 
          u=None          , du=None           , mu=None,
          v=None          , dv=Decimal('5')   , mv=None,
          implied=True)
        # Value 4: Negative
        meas_meas_div(
          x=-4            , dx=2              , xu=Unit(), 
          y=-3            , dy=None           , yu=Unit(), 
          u=None          , du=None           , mu=None,
          v=None          , dv=Decimal('0.5') , mv=None,
          implied=True)
        # Value 5: Zero
        if(True):
          # Int
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 4,2,Unit()
            y,dy,yu = 0,None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Float
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 0.4,0.2,Unit()
            y,dy,yu = 0.0,None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Decimal 
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
            y,dy,yu = Decimal("0.0"),None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2) 
          b = Measure(value=3,error=None)
          c = a/b
          c = None
          assert a == Measure(value=4,error=2) 
          assert b == Measure(value=3,error=None)
      # Unitless / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit(), 
            y=3             , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit(), 
            y=0.3           , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit(), 
            y=-3            , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit()
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit()
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit(), 
            y=3             , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit(), 
            y=0.3           , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit(), 
            y=Decimal("30") , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit(), 
            y=-3            , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5')   , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit()
              y,dy,yu = 0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit()
              y,dy,yu = 0.0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit()
              y,dy,yu = Decimal("0.0"),None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=2              , xu=Unit(), 
            y=27                , dy=None           , yu=Unit("\u00B0C"), 
            u=None              , du=None           , mu=None,
            v=Decimal("300.15") , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=299.9             , dx=0.02           , xu=Unit(), 
            y=26.85             , dy=None           , yu=Unit("\u00B0C"), 
            u=None              , du=None           , mu=None,
            v=300.0             , dv=0.005          , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=Decimal("0.02")  , xu=Unit(), 
            y=Decimal("26.85")  , dy=None             , yu=Unit("\u00B0C"), 
            u=None              , du=None             , mu=None,
            v=Decimal("300")    , dv=Decimal('0.005') , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=300               , dx=2              , xu=Unit(), 
            y=-27               , dy=None           , yu=Unit("\u00B0C"), 
            u=None              , du=None           , mu=None,
            v=Decimal("246.15") , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=300               , dx=2              , xu=Unit(), 
              y=0                 , dy=None           , yu=Unit("\u00B0C"), 
              u=None              , du=None           , mu=None,
              v=Decimal("273.15") , dv=Decimal('0.5') , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=300.0             , dx=0.02           , xu=Unit(), 
              y=0.0               , dy=None           , yu=Unit("\u00B0C"), 
              u=None              , du=None           , mu=None,
              v=273.15            , dv=0.05            , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("300")    , dx=Decimal("0.02"), xu=Unit(), 
              y=Decimal("0")      , dy=None           , yu=Unit("\u00B0C"), 
              u=None              , du=None           , mu=None,
              v=Decimal("273.15") , dv=Decimal('0.5') , mv=None,
              implied=True)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2) 
          b = Measure(value=3,error=None,unit=Unit("cm"))
          c = a/b
          c = None
          assert a == Measure(value=4,error=2) 
          assert b == Measure(value=3,error=None,unit=Unit("cm"))
      # Unit / Unitless
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit("cm"), 
            y=3             , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit("cm"), 
            y=0.3           , dy=None           , yu=Unit(),
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
            y=Decimal("30") , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit("cm"), 
            y=-3            , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("cm")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("cm")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("cm")
              y,dy,yu = Decimal("0.0"),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit("5 m^2"), 
            y=3             , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit("5 m^2"), 
            y=0.3           , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("5 m^2"), 
            y=Decimal("30") , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit("5 m^2"), 
            y=-3            , dy=None           , yu=Unit(), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("5 m^2")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("5 m^2")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("5 m^2")
              y,dy,yu = Decimal("0.0"),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=27                , dx=1               , xu=Unit("\u00B0C"), 
            y=300               , dy=None            , yu=Unit(), 
            u=Decimal("300.15") , du=None            , mu=None,
            v=None              , dv=Decimal('50')   , mv=None,
            value = Decimal("300.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=26.85         , dx=0.01           , xu=Unit("\u00B0C"), 
            y=299.9         , dy=None           , yu=Unit(), 
            u=300.0         , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            value  = 300.0/299.9-273.15,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("26.85"), dx=Decimal("0.01"), xu=Unit("\u00B0C"), 
            y=Decimal("300")  , dy=None           , yu=Unit(), 
            u=Decimal("300")  , du=None           , mu=None,
            v=None            , dv=Decimal('50')  , mv=None,
            value = 1+ Decimal("-273.15"),
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-27               , dx=1              , xu=Unit("\u00B0C"), 
            y=300               , dy=None           , yu=Unit(), 
            u=Decimal("246.15") , du=None           , mu=None,
            v=None              , dv=Decimal('50')  , mv=None,
            value = Decimal("246.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 27,2,Unit("\u00B0C")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 26.15,0.02,Unit("\u00B0C")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("26.15"),Decimal("0.02"),Unit("\u00B0C")
              y,dy,yu = Decimal(0),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=2,unit=Unit("cm")) 
          b = Measure(value=3,error=None)
          c = a/b
          c = None
          assert a == Measure(value=4,error=2,unit=Unit("cm")) 
          assert b == Measure(value=3,error=None)
      # Unit / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit("s"), 
            y=3             , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit("s"), 
            y=0.3           , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("s"), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit("s"), 
            y=-3            , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("s")
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("s")
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("s")
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit("2 s"), 
            y=3             , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit("2 s"), 
            y=0.3           , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("2 s"), 
            y=Decimal("30") , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit("2 s"), 
            y=-3            , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("2 s")
              y,dy,yu = 0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("2 s")
              y,dy,yu = 0.0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("2 s")
              y,dy,yu = Decimal("0.0"),None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=2              , xu=Unit("s"), 
            y=27                , dy=None           , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=None           , mu=None,
            v=Decimal("300.15") , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=300.0 , dx=0.02   , xu=Unit("s"), 
            y=26.85 , dy=None   , yu=Unit("\u00B0C"), 
            u=300.0 , du=None   , mu=None,
            v=300.0 , dv=0.005  , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=Decimal("0.02")  , xu=Unit("s"), 
            y=Decimal("26.85")  , dy=None             , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=None             , mu=None,
            v=Decimal("300")    , dv=Decimal('0.005') , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-31               , dx=2              , xu=Unit("m"), 
            y=-27               , dy=None           , yu=Unit("\u00B0C"), 
            u=Decimal("-31")    , du=None           , mu=None,
            v=Decimal("246.15") , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=27                , dx=2              , xu=Unit("\u00B0C"), 
              y=0                 , dy=None           , yu=Unit("\u00B0C"), 
              u=Decimal("300.15") , du=None           , mu=None,
              v=Decimal("273.15") , dv=Decimal('0.5') , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=26.85   , dx=0.02 , xu=Unit("\u00B0C"), 
              y= 0.0    , dy=None , yu=Unit("\u00B0C"), 
              u=300.0   , du=None , mu=None,
              v=273.15  , dv=0.05 , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("26.85")  , dx=Decimal("0.02")  , xu=Unit("\u00B0C"), 
              y=Decimal("0")      , dy=None             , yu=Unit("\u00B0C"), 
              u=Decimal("300")    , du=None             , mu=None,
              v=Decimal("273.15") , dv=Decimal('0.5')   , mv=None,
              implied=True)
        # Canceling Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4             , dx=2              , xu=Unit("cm"), 
            y=3             , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4           , dx=0.2            , xu=Unit("cm"), 
            y=0.3           , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=Decimal("20")  , xu=Unit("cm"), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('5')   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4            , dx=2              , xu=Unit("cm"), 
            y=-3            , dy=None           , yu=Unit("cm"), 
            u=None          , du=None           , mu=None,
            v=None          , dv=Decimal('0.5') , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,2,Unit("cm")
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,0.2,Unit("cm")
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),Decimal("0.2"),Unit("cm")
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
    # Measure (Implicit Error) / Measure (Explicit Error) = Measure (Implicit Error)
    if(True):
      # Unitless / Unitless
      if(True):
        # Value 1: Int
        meas_meas_div(
          x=4     , dx=None              , xu=Unit(), 
          y=3     , dy=1              , yu=Unit(), 
          u=None  , du=Decimal("0.5") , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 2: Float
        meas_meas_div(
          x=0.4   , dx=None           , xu=Unit(), 
          y=0.3   , dy=0.1            , yu=Unit(), 
          u=None  , du=0.05           , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 3: Decimal
        meas_meas_div(
          x=Decimal("40") , dx=None           , xu=Unit(), 
          y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
          u=None          , du=Decimal("5")   , mu=None,
          v=None          , dv=None           , mv=None,
          implied=True)
        # Value 4: Negative
        meas_meas_div(
          x=-4    , dx=None           , xu=Unit(), 
          y=-3    , dy=1              , yu=Unit(),
          u=None  , du=Decimal("0.5") , mu=None,
          v=None  , dv=None           , mv=None,
          implied=True)
        # Value 5: Zero
        if(True):
          # Int
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 4,None,Unit()
            y,dy,yu = 0,1,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Float
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 0.4,None,Unit()
            y,dy,yu = 0.0,0.1,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Decimal 
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = Decimal("0.4"),None,Unit()
            y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None) 
          b = Measure(value=3,error=2)
          c = a/b
          c = None
          assert a == Measure(value=4,error=None) 
          assert b == Measure(value=3,error=2)
      # Unitless / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None              , xu=Unit(), 
            y=3     , dy=1              , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit(), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit(), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit(), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit()
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit()
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit()
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit(), 
            y=3     , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit(), 
            y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit(), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit(), 
            y=-3    , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit()
              y,dy,yu = 0,1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit()
              y,dy,yu = 0.0,0.1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit()
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=None           , xu=Unit(), 
            y=27                , dy=1              , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50") , mu=None,
            v=Decimal("300.15") , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=299.9 , dx=None , xu=Unit(), 
            y=26.85 , dy=0.01 , yu=Unit("\u00B0C"), 
            u=None  , du=0.05 , mu=None,
            v=300.0 , dv=None , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=None             , xu=Unit(), 
            y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50")    , mu=None,
            v=Decimal("300")    , dv=None             , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=300               , dx=None           , xu=Unit(), 
            y=-27               , dy=1              , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50")  , mu=None,
            v=Decimal("246.15") , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=300               , dx=None           , xu=Unit(), 
              y=0                 , dy=1              , yu=Unit("\u00B0C"), 
              u=None              , du=Decimal("50")  , mu=None,
              v=Decimal("273.15") , dv=None           , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=300.0   , dx=None , xu=Unit(), 
              y=0.0     , dy=0.01 , yu=Unit("\u00B0C"), 
              u=None    , du=0.05 , mu=None,
              v=273.15  , dv=None , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("300")    , dx=None             , xu=Unit(), 
              y=Decimal("0")      , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
              u=None              , du=Decimal("50")    , mu=None,
              v=Decimal("273.15") , dv=None             , mv=None,
              implied=True)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None) 
          b = Measure(value=3,error=2,unit=Unit("cm"))
          c = a/b
          c = None
          assert a == Measure(value=4,error=None) 
          assert b == Measure(value=3,error=2,unit=Unit("cm"))
      # Unit / Unitless
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None              , xu=Unit("cm"), 
            y=3     , dy=1              , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("cm"), 
            y=0.3   , dy=0.1            , yu=Unit(), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("cm"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("cm"), 
            y=-3    , dy=1              , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("cm")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("cm")
              y,dy,yu = 0.0,0.1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("cm")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("5 m^2"), 
            y=3     , dy=1              , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("5 m^2"), 
            y=0.3   , dy=0.1            , yu=Unit(), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("5 m^2"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit(), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("5 m^2"), 
            y=-3    , dy=1              , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("5 m^2")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("5 m^2")
              y,dy,yu = 0.0,0.1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("5 m^2")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=27                , dx=None           , xu=Unit("\u00B0C"), 
            y=300               , dy=2              , yu=Unit(), 
            u=Decimal("300.15") , du=Decimal("0.5") , mu=None,
            v=None              , dv=None           , mv=None,
            value = Decimal("300.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=26.85 , dx=None  , xu=Unit("\u00B0C"), 
            y=299.9 , dy=0.02  , yu=Unit(), 
            u=300.0 , du=0.005 , mu=None,
            v=None  , dv=None  , mv=None,
            value  = 300.0/299.9-273.15,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("26.85")  , dx=None             , xu=Unit("\u00B0C"), 
            y=Decimal("300")    , dy=Decimal("0.02")  , yu=Unit(), 
            u=Decimal("300")    , du=Decimal("0.005") , mu=None,
            v=None              , dv=None             , mv=None,
            value = 1+Decimal("-273.15"),
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-27               , dx=None           , xu=Unit("\u00B0C"), 
            y=300               , dy=2              , yu=Unit(), 
            u=Decimal("246.15") , du=Decimal("0.5") , mu=None,
            v=None              , dv=None           , mv=None,
            value = Decimal("246.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 27,None,Unit("\u00B0C")
              y,dy,yu = 0,1,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 26.15,None,Unit("\u00B0C")
              y,dy,yu = 0.0,0.01,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("26.15"),None,Unit("\u00B0C")
              y,dy,yu = Decimal(0),Decimal("0.01"),Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None,unit=Unit("cm")) 
          b = Measure(value=3,error=2)
          c = a/b
          c = None
          assert a == Measure(value=4,error=None,unit=Unit("cm")) 
          assert b == Measure(value=3,error=2)
      # Unit / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("s"), 
            y=3     , dy=1              , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None            , xu=Unit("s"), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("s"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("s"), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("s")
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("s")
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("s")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("2 s"), 
            y=3     , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("2 s"), 
            y=0.3   , dy=0.1            , yu=Unit("5 m^2"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None  , xu=Unit("2 s"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("5 m^2"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("2 s"), 
            y=-3    , dy=1              , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("2 s")
              y,dy,yu = 0,1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("2 s")
              y,dy,yu = 0.0,0.1,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("2 s")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=None           , xu=Unit("s"), 
            y=27                , dy=1              , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=Decimal("50")  , mu=None,
            v=Decimal("300.15") , dv=None           , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=300.0 , dx=None , xu=Unit("s"), 
            y=26.85 , dy=0.01 , yu=Unit("\u00B0C"), 
            u=300.0 , du=0.05 , mu=None,
            v=300.0 , dv=None , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=None             , xu=Unit("s"), 
            y=Decimal("26.85")  , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=Decimal("50")    , mu=None,
            v=Decimal("300")    , dv=None             , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-31               , dx=None           , xu=Unit("m"), 
            y=-27               , dy=1              , yu=Unit("\u00B0C"), 
            u=Decimal("-31")    , du=Decimal("0.5") , mu=None,
            v=Decimal("246.15") , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=27                , dx=None           , xu=Unit("\u00B0C"), 
              y=0                 , dy=1              , yu=Unit("\u00B0C"), 
              u=Decimal("300.15") , du=Decimal("0.5") , mu=None,
              v=Decimal("273.15") , dv=None           , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=26.85   , dx=None   , xu=Unit("\u00B0C"), 
              y= 0.0    , dy=0.01   , yu=Unit("\u00B0C"), 
              u=300.0   , du=0.005  , mu=None,
              v=273.15  , dv=None   , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("26.85")  , dx=None             , xu=Unit("\u00B0C"), 
              y=Decimal("0")      , dy=Decimal("0.01")  , yu=Unit("\u00B0C"), 
              u=Decimal("300")    , du=Decimal("0.005") , mu=None,
              v=Decimal("273.15") , dv=None             , mv=None,
              implied=True)
        # Canceling Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("cm"), 
            y=3     , dy=1              , yu=Unit("cm"),
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None, 
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("cm"), 
            y=0.3   , dy=0.1            , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("cm"), 
            y=Decimal("30") , dy=Decimal("10")  , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=None           , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("cm"), 
            y=-3    , dy=1              , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=None           , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("cm")
              y,dy,yu = 0,1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("cm")
              y,dy,yu = 0.0,0.1,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("cm")
              y,dy,yu = Decimal("0.0"),Decimal("0.1"),Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
    # Measure (Implicit Error) / Measure (Implicit Error) = Measure (Implicit Error)
    if(True):
      # Unitless / Unitless
      if(True):
        # Value 1: Int
        meas_meas_div(
          x=4     , dx=None             , xu=Unit(), 
          y=3     , dy=None             , yu=Unit(), 
          u=None  , du=Decimal("0.5")   , mu=None,
          v=None  , dv=Decimal("0.5")   , mv=None,
          implied=True)
        # Value 2: Float
        meas_meas_div(
          x=0.4   , dx=None           , xu=Unit(), 
          y=0.3   , dy=None           , yu=Unit(), 
          u=None  , du=0.05           , mu=None,
          v=None  , dv=0.05           , mv=None,
          implied=True)
        # Value 3: Decimal
        meas_meas_div(
          x=Decimal("40") , dx=None           , xu=Unit(), 
          y=Decimal("30") , dy=None           , yu=Unit(), 
          u=None          , du=Decimal("5")   , mu=None,
          v=None          , dv=Decimal("5")   , mv=None,
          implied=True)
        # Value 4: Negative
        meas_meas_div(
          x=-4    , dx=None           , xu=Unit(), 
          y=-3    , dy=None           , yu=Unit(),
          u=None  , du=Decimal("0.5") , mu=None,
          v=None  , dv=Decimal("0.5") , mv=None,
          implied=True)
        # Value 5: Zero
        if(True):
          # Int
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 4,None,Unit()
            y,dy,yu = 0,None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Float
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = 0.4,None,Unit()
            y,dy,yu = 0.0,None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
          # Decimal 
          with pytest.raises(Exception):
            # Context Values
            x,dx,xu = Decimal("0.4"),None,Unit()
            y,dy,yu = Decimal("0.0"),None,Unit()
            # Error Out
            Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None) 
          b = Measure(value=3,error=None)
          c = a/b
          c = None
          assert a == Measure(value=4,error=None) 
          assert b == Measure(value=3,error=None)
      # Unitless / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None              , xu=Unit(), 
            y=3     , dy=None           , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit(), 
            y=0.3   , dy=None           , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit(), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit(), 
            y=-3    , dy=None           , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit()
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit()
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit()
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit(), 
            y=3     , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit(), 
            y=0.3   , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit(), 
            y=Decimal("30") , dy=None           , yu=Unit("5 m^2"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit(), 
            y=-3    , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit()
              y,dy,yu = 0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit()
              y,dy,yu = 0.0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit()
              y,dy,yu = Decimal("0.0"),None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=None           , xu=Unit(), 
            y=27                , dy=None           , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50")  , mu=None,
            v=Decimal("300.15") , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=299.9 , dx=None   , xu=Unit(), 
            y=26.85 , dy=None   , yu=Unit("\u00B0C"), 
            u=None  , du=0.05   , mu=None,
            v=300.0 , dv=0.005  , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=None             , xu=Unit(), 
            y=Decimal("26.85")  , dy=None             , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50")    , mu=None,
            v=Decimal("300")    , dv=Decimal("0.005") , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=300               , dx=None           , xu=Unit(), 
            y=-27               , dy=None           , yu=Unit("\u00B0C"), 
            u=None              , du=Decimal("50")  , mu=None,
            v=Decimal("246.15") , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=300               , dx=None           , xu=Unit(), 
              y=0                 , dy=None           , yu=Unit("\u00B0C"), 
              u=None              , du=Decimal("50")  , mu=None,
              v=Decimal("273.15") , dv=Decimal("0.5") , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=300.0   , dx=None , xu=Unit(), 
              y=0.0     , dy=None , yu=Unit("\u00B0C"), 
              u=None    , du=0.05 , mu=None,
              v=273.15  , dv=0.05 , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("300")    , dx=None             , xu=Unit(), 
              y=Decimal("0")      , dy=None             , yu=Unit("\u00B0C"), 
              u=None              , du=Decimal("50")    , mu=None,
              v=Decimal("273.15") , dv=Decimal("0.5")   , mv=None,
              implied=True)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None) 
          b = Measure(value=3,error=None,unit=Unit("cm"))
          c = a/b
          c = None
          assert a == Measure(value=4,error=None) 
          assert b == Measure(value=3,error=None,unit=Unit("cm"))
      # Unit / Unitless
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None              , xu=Unit("cm"), 
            y=3     , dy=None           , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("cm"), 
            y=0.3   , dy=None           , yu=Unit(), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("cm"), 
            y=Decimal("30") , dy=None           , yu=Unit(), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("cm"), 
            y=-3    , dy=None           , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("cm")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("cm")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("cm")
              y,dy,yu = Decimal("0.0"),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("5 m^2"), 
            y=3     , dy=None           , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("5 m^2"), 
            y=0.3   , dy=None           , yu=Unit(), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("5 m^2"), 
            y=Decimal("30") , dy=None           , yu=Unit(), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("5 m^2"), 
            y=-3    , dy=None           , yu=Unit(), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("5 m^2")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("5 m^2")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("5 m^2")
              y,dy,yu = Decimal("0.0"),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=27                , dx=None           , xu=Unit("\u00B0C"), 
            y=300               , dy=None           , yu=Unit(), 
            u=Decimal("300.15") , du=Decimal("0.5") , mu=None,
            v=None              , dv=Decimal("50")  , mv=None,
            value = Decimal("300.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=26.85 , dx=None  , xu=Unit("\u00B0C"), 
            y=299.9 , dy=None  , yu=Unit(), 
            u=300.0 , du=0.005 , mu=None,
            v=None  , dv=0.05  , mv=None,
            value  = 300.0/299.9-273.15,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("26.85")  , dx=None             , xu=Unit("\u00B0C"), 
            y=Decimal("300")    , dy=None             , yu=Unit(), 
            u=Decimal("300")    , du=Decimal("0.005") , mu=None,
            v=None              , dv=Decimal("50")    , mv=None,
            value = 1+Decimal("-273.15"),
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-27               , dx=None           , xu=Unit("\u00B0C"), 
            y=300               , dy=None           , yu=Unit(), 
            u=Decimal("246.15") , du=Decimal("0.5") , mu=None,
            v=None              , dv=Decimal("50")  , mv=None,
            value = Decimal("246.15")/Decimal("300") - Decimal("273.15"),
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 27,None,Unit("\u00B0C")
              y,dy,yu = 0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 26.15,None,Unit("\u00B0C")
              y,dy,yu = 0.0,None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("26.15"),None,Unit("\u00B0C")
              y,dy,yu = Decimal(0),None,Unit()
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Preserve Inputs
        if(True):
          a = Measure(value=4,error=None,unit=Unit("cm")) 
          b = Measure(value=3,error=None)
          c = a/b
          c = None
          assert a == Measure(value=4,error=None,unit=Unit("cm")) 
          assert b == Measure(value=3,error=None)
      # Unit / Unit
      if(True):
        # Normal Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("s"), 
            y=3     , dy=None           , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None            , xu=Unit("s"), 
            y=0.3   , dy=None           , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("s"), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("s"), 
            y=-3    , dy=None           , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("s")
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("s")
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("s")
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Magnitude Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("2 s"), 
            y=3     , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("2 s"), 
            y=0.3   , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None  , xu=Unit("2 s"), 
            y=Decimal("30") , dy=None  , yu=Unit("5 m^2"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("2 s"), 
            y=-3    , dy=None           , yu=Unit("5 m^2"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("2 s")
              y,dy,yu = 0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("2 s")
              y,dy,yu = 0.0,None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("2 s")
              y,dy,yu = Decimal("0.0"),None,Unit("5 m^2")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
        # Convoluted Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=300               , dx=None           , xu=Unit("s"), 
            y=27                , dy=None           , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=Decimal("50")  , mu=None,
            v=Decimal("300.15") , dv=Decimal("0.5")  , mv=None,
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=300.0 , dx=None   , xu=Unit("s"), 
            y=26.85 , dy=None   , yu=Unit("\u00B0C"), 
            u=300.0 , du=0.05   , mu=None,
            v=300.0 , dv=0.005  , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("300")    , dx=None             , xu=Unit("s"), 
            y=Decimal("26.85")  , dy=None             , yu=Unit("\u00B0C"), 
            u=Decimal("300")    , du=Decimal("50")    , mu=None,
            v=Decimal("300")    , dv=Decimal("0.005") , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-31               , dx=None           , xu=Unit("m"), 
            y=-27               , dy=None           , yu=Unit("\u00B0C"), 
            u=Decimal("-31")    , du=Decimal("0.5") , mu=None,
            v=Decimal("246.15") , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            meas_meas_div(
              x=27                , dx=None           , xu=Unit("\u00B0C"), 
              y=0                 , dy=None           , yu=Unit("\u00B0C"), 
              u=Decimal("300.15") , du=Decimal("0.5") , mu=None,
              v=Decimal("273.15") , dv=Decimal("0.5") , mv=None,
              implied=True)
            # Float
            meas_meas_div(
              x=26.85   , dx=None   , xu=Unit("\u00B0C"), 
              y= 0.0    , dy=None   , yu=Unit("\u00B0C"), 
              u=300.0   , du=0.005  , mu=None,
              v=273.15  , dv=0.05   , mv=None,
              implied=True)
            # Decimal
            meas_meas_div(
              x=Decimal("26.85")  , dx=None             , xu=Unit("\u00B0C"), 
              y=Decimal("0")      , dy=None             , yu=Unit("\u00B0C"), 
              u=Decimal("300")    , du=Decimal("0.005") , mu=None,
              v=Decimal("273.15") , dv=Decimal("0.5")   , mv=None,
              implied=True)
        # Canceling Units
        if(True):
          # Value 1: Int
          meas_meas_div(
            x=4     , dx=None           , xu=Unit("cm"), 
            y=3     , dy=None           , yu=Unit("cm"),
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None, 
            implied=True)
          # Value 2: Float
          meas_meas_div(
            x=0.4   , dx=None           , xu=Unit("cm"), 
            y=0.3   , dy=None           , yu=Unit("cm"), 
            u=None  , du=0.05           , mu=None,
            v=None  , dv=0.05           , mv=None,
            implied=True)
          # Value 3: Decimal
          meas_meas_div(
            x=Decimal("40") , dx=None           , xu=Unit("cm"), 
            y=Decimal("30") , dy=None           , yu=Unit("cm"), 
            u=None          , du=Decimal("5")   , mu=None,
            v=None          , dv=Decimal("5")   , mv=None,
            implied=True)
          # Value 4: Negative
          meas_meas_div(
            x=-4    , dx=None           , xu=Unit("cm"), 
            y=-3    , dy=None           , yu=Unit("cm"), 
            u=None  , du=Decimal("0.5") , mu=None,
            v=None  , dv=Decimal("0.5") , mv=None,
            implied=True)
          # Value 5: Zero
          if(True):
            # Int
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 4,None,Unit("cm")
              y,dy,yu = 0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Float
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = 0.4,None,Unit("cm")
              y,dy,yu = 0.0,None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
            # Decimal 
            with pytest.raises(Exception):
              # Context Values
              x,dx,xu = Decimal("0.4"),None,Unit("cm")
              y,dy,yu = Decimal("0.0"),None,Unit("cm")
              # Error Out
              Measure(value=x,error=dx,unit=xu)  /  Measure(value=y,error=dy,unit=yu)
    
    
  def test_div(self):
    
    # Unit
    if(True):
      # Canceling
      assert Measure("4(2)cm")   / Unit("cm/$")       == Measure("4(2)$")
      assert (Unit("cm/$")/Measure("3(1)cm")).approx(Measure("0.33333(11111)/$"))
      
    # Number
    if(True):
      # Values & Certainties
      assert Measure("4(2)cm") / Decimal("2") == Measure("2(1)cm")
      assert Measure("4(2)cm") /         "2"  == Measure("2(1)cm")
      assert Measure("4(2)cm") /          2   == Measure("2(1)cm")
      assert (Decimal("2") / Measure("3(1)cm")).approx(Measure("0.66666(22222)cm^-1"))
      assert (        "2"  / Measure("3(1)cm")).approx(Measure("0.66666(22222)cm^-1"))
      assert (         2   / Measure("3(1)cm")).approx(Measure("0.66666(22222)cm^-1"))
      # Implied Uncertainty
      assert (Measure("3cm")  / Decimal("2")).implied == True
      assert (Measure("3cm")  /         "2" ).implied == True
      assert (Measure("3cm")  /          2  ).implied == True
      # Divide by Zero Errors
      with pytest.raises(Exception):
        assert Measure("3cm")  / Decimal("0")
      with pytest.raises(Exception):
        assert Measure("3cm")  / "0"
      with pytest.raises(Exception):
        assert Measure("3cm")  / 0
    # String Measure
    if(True):
      # Values, Certainties, Canceling
      assert (Measure("3(1)cm") / "4(2)cm").approx(Measure("0.75(45)"))
      assert ("3(1)cm" / Measure("4(2)cm")).approx(Measure("0.75(45)"))
      # Implied Uncertainty
      assert (Measure("3cm") / "4(2)cm").implied == True
      assert ("3cm" / Measure("4(2)cm")).implied == True
      assert Measure("5 m^2",value="2") / "5 m^2" == Measure("2")
      assert "20 m^2" / Measure("5 m^2",value="2") == Measure("2")
      # Divide By Zero
      with pytest.raises(Exception):
        Measure("3 cm")/"0 m"
      with pytest.raises(Exception):
        "3 cm"/Measure("0 m")
      # Weird unitss 
      assert Measure("26.85 \u00B0C") / "26.85 \u00B0C" == Measure("1")
      assert "26.85 \u00B0C" / Measure("26.85 \u00B0C") == Measure("1")
      assert Measure("5 carrot") / "1 pig" == Measure("5 carrot / pig")
      assert "5 carrot" / Measure("1 pig") == Measure("5 carrot / pig")
      # Past Failed Units
      assert (Measure("5cm")/"1 min").units == Unit("cm/min")
      assert ("5cm"/Measure("1 min")).units == Unit("cm/min")
  
  # Exponents
  def test_power(self):
    # set-up
    a = Measure("4(2)cm")
    b = Measure("6(1)cm/cm")
    three = Decimal("3")
    c = Measure("4096(13536)cm^6")
    d = Measure("64(96)cm^3")
    e = Measure("729(800)")
    # assert
    assert (a**b).approx(c)
    assert (a**three).approx(d)
    assert (three**b).approx(e)
    # Implied Uncertainty
    f = Measure("4")
    g = Measure("6")
    assert (f**g).implied == True
    assert (f**three).implied == True
    # Exceptions
    with pytest.raises(Exception):
      Measure("0")**Measure("0")
  def test_log(self):
    assert Measure.log(Measure("6(1)"),base=Measure("4(2)")).approx(Measure("1(2.97)"))
    assert Measure.log(Decimal("3"),   base=Measure("4(2)")).approx(Measure("1.26(43)"))
    assert Measure.log(Measure("6(1)"),base=Decimal("3")   ).approx(Measure("1.63(2)"))
    # Implied Uncertainty
    f = Measure("4")
    g = Measure("6")
    assert Measure.log(g,base=f).implied == True
    assert Measure.log(3,base=f).implied == True
    # Exceptions
    with pytest.raises(IncompatibleUnitException):
      Measure.log(Measure("12 mg"),base=Measure("2 mg"))
  
  # Trigonometry
  def test_sin(self):
    # Radians
    a = Measure("3.14(5)")
    b = Measure("0.0016(25)")# +- 0.0025
    c = Measure("3.14")
    assert a.sin().approx(b)
    assert c.sin().implied == True
    # Degrees
    a = Measure("90 deg")
    b = Measure("1")
    assert a.sin().approx(b)
    # Exceptions
    with pytest.raises(IncompatibleUnitException):
      Measure.sin(Measure("12 mg"))
    # Exceptions Radiation Rads
    with pytest.raises(IncompatibleUnitException):
      Measure.sin(Measure("12 rad"))
  def test_cos(self):
    # Radians
    a = Measure("3.5(1)")
    b = Measure("-0.936(1)")# -0.9364 +- 0.0025
    c = Measure("3.5")
    assert a.cos().approx(b)
    assert c.cos().implied == True
    # Degrees
    a = Measure("90 deg")
    b = Measure("0")
    assert a.cos().approx(b)
    # Exceptions
    with pytest.raises(IncompatibleUnitException):
      Measure.cos(Measure("12 mg"))
    # Exceptions Radiation Rads
    with pytest.raises(IncompatibleUnitException):
      Measure.cos(Measure("12 rad"))
  
  #
  def test_round(self):
    a = Measure("0.0016(26)")# +- 0.0025
    b = Measure("0.002(3)")
    assert b == round(a,3)
    assert round(Measure("12.34cm")).implied == True
    assert round(Measure("12.34(2)cm")).implied == False
  
  # 
  def test_in(self):
    assert not ( Measure("300") in [True] )
  