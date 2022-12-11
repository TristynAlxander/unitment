# Unitment

The `unitment` module provides support for dynamic unit (and error) management through `Unit` and `Measure` classes.
The guiding philosophy of the module is to focus users on their maths, not units or code.
The module is built to allow users to forget about units and unit management. 
To that end, the module is extremely dynamic in many ways that provide notable advantages over other unit management modules:

 - Unit Compatibility. This module works with *almost any* units. 
 While metric units are used by default, imperial units are defined as a class constant (`Measure("degF",Unit.IMPERIAL_UNITS)`). 
 Arbitrary units can be used as their own (non-physical) dimension without being explicitly defined - albeit without prefixes, conversion-functions, or decompositions. 
 More advanced units can easily be loaded or defined for automatic conversion to base-units and the unit definitions propagate with the units themselves.
 Indeed, some advanced units (pH, Celsius) are already defined.
 
 - Intuitive Instantiation. Units and Measures are made with easy constructors in this package: e.g. `Measure("5 m")`, `Measure(5,"m")`, `Measure(value=5,units="m")`, etc.
 Users needn't familiarize themselves with a cluttered or convoluted namespace or even understand much python or coding in general. 
 Again, the goal is to allow the users to focus on their maths in abstract-terms that maintain perspective on their problem, rather than dragging unit-hell into coding. 
 
 - Math in Dimensions. Each Unit and Measure automatically decomposes and simplifies to base-unit form prior to preforming mathematical operations.
 This allows math to be done in terms of the actual base-dimensions, which is crucial for some units (e.g. ℃). 
 Where possible, the original units are retained for the final result. 
 As a result, users needn't think in terms of units after they've been defined. 
 Users may focus on doing math in the more abstract terms or at the level of the dimension. 
 
 - Propagation of Error. Propagation of error is built into every operator.
 While this is a worst-case (non-abstract) error calculation, it helps users gain a grasp on the reliability-of and precision-needed-for their system.

 - Low Over-head. A lot of effort was put into preventing the module from being slow. 
 While it could be faster at cost of code maintainability or usability, it is quite fast for what it does.
 Moreover, the module's only dependencies are in the Python Standard Library (Mostly the `math` and `decimal` modules). 
 Overall, this module is well suited for scripting purposes. 

All that said, the choice of unit management module does depend on use-case. 
The general advise for users is to use this module for scripting simple math or conversions. 
While this module may work for surprisingly complicated things, we recommend removing units altogether for advanced applications. 
In such cases, this module may still be useful as a parser. 

____________________________________________________________

Consider supporting unitment on [patreon](www.patreon.com/user?u=83796428).

____________________________________________________________

# Quick Install

`pip install unitment`

# Quick Start Example

    from unitment import Unit,Measure
    
    distance = Measure("25 m")
    time     = Measure("5 s")
    speed    = distance / time
    

____________________________________________________________


## Measure

`Measure` is the primary class in this package. Measures have a value, a unit, and an error. The error is often implied. 
This class reflects the logical structure in its properties: `value`, `units`, and `error`. Likewise, the error is inferred if not explicitly provided. 
The value and unit properties are numbers. The unit is defined more extensively below.

**Instantiation:** 
This class is built to be instantiated casually and intuitively, e.g. `Measure("25 m")`, so reasonable string inputs should be processed as expected.
That said, care should be taken to leave a space between symbols as milliseconds (`"ms"`) are quite different from meter seconds (`"m s"`).
Beyond that, the parser is fairly robust. It is generally capable of handling exponents and error notations. 
The class can also be instantiated with the keywords `value`, `error`, and `unit` or `units`.

**Dominant:** The Measure class dominates in mathematical operations, so a float * Measure = Measure. 
For very large programs with very large numbers of operations, this will slow down the program. 
For maximum efficiency, it's always better to use this package as a parser and converter then cast the measure as a float.

For example:

    x_raw    = "2583 cm"
    x_meters = float(Measure(x_raw).convert("m"))

### Value

The class will accept and Number or would-be number as a value. This includes Decimals, floats, ints, and strings that can be converted to decimals.
Internally the class will preserve Decimals until it encounters a float mathematical operations, at which point all internal values will convert to floats. 
If inputting the value as an argument rather than a keyword or parsed string, the first number will be considered the value, the second the error.

### Error

**Definition of Error:** This module defines error as the square root of the variance: the standard deviation.

**Numerical Error Assumption:**
Since the module is not context-aware, propagation of error occurs with the assumption of numerical (and thus non-canceling) inputs for every operation.
This worse-case assumption is used because the module cannot be aware of its analytical context.
For example, analytically one knows that a - b + b = a.
Without context-awareness, the 'big-picture' cannot be observed and the module must operate numerically.
The module (like most code) sees (a-b), solves this as c, sees (c+b), and solves that. Propagation of error occurs at each step.
As a result, extra propagation of error occurs where none should exist in analytical contexts.

**Propagation of Error Equations:** 
The propagation of error equation (the taylor-series expansion of the statistical moments) for a function with two inputs is as follows:

var(f) = (∂f/∂x)^2 var(x) + (∂f/∂x) (∂f/∂y) covar(x) + (∂f/∂y)^2 var(y)

Since the module is not context-aware, it must assume independent inputs; thus, this equation is more appropriate:

var(f) = (∂f/∂x)^2 var(x) + (∂f/∂y)^2 var(y)

That is the equation used by the module. For edification of the reader, this equation can be extended to multi-input function as follows:

var(f) = Σ (∂f/∂xi)^2 var(xi)

**Propagation of Error Failures:** 
Since each of these are essentially the same equation all-be-it in slightly different contexts, they share the requirements of taylor-series expansions. 
Namely, the functions must be sufficiently differentiable and the approximations must be sufficiently local. 
The floor, ceil, and round functions are not sufficiently differentiable for the taylor series expansions for the moments to be valid. 
Given this and that most users would not be using them in a mathematically rigorous context, these functions do not propagate error properly. 
The modulo function is defined in terms of the floor function (i.e. x % y = x-y*floor(x/y)); thus, it also does not propagate error properly. 
Other non-linear functions (such as log) are likely accurate locally (for very small errors), but are at greater risk of inaccuracies as values increase.

**Implied Errors:**
For implied errors of given values (i.e. `Measure(10.0,"m")`), the module gives it's best guess by converting the value to a string.
This can produce incorrect results with floats (e.g. `Measure(float(10),"m")`). 
As such, if concerned with error inputting values as strings or Decimal is recommended when not defining the error explicitly with keywords.


### Restrictions on Mathematics

Restrictions are put on the mathematics due to the presence of units. These should all be fairly intuitive.
The most obvious restriction is that measurements with different units cannot be added together. 
One can use a simple taylor series to show that this restriction implies that units must cancel in exponents. 

## Units

Units are labels for self-consistent chunks of dimensions. 
These dimensions can be physical, non-physical, or even complex abstractions. 
Despite the possible dimensions, units have a consistent logic-structure. 
This allows them to be defined and categorized by complexity:

- **Base Unit:**     Base     Units are singular and cannot be converted into other units. Examples: `"m"`, `"fish"`.
- **Derived Unit:**  Derived  Units are singular but can    be converted into other units. Examples: `"cm"`, `"J"`.
- **Compound Unit:** Compound Units are multiple logically related units. Examples: `"cm / fish"`, `"J / m"`

The `Unit` class is for base, derived, or compound units with multiple base-dimensions and/or magnitude modifiers. 
Here, the term "symbol" or "symbols" refers to a singular unit (base-unit or derived-unit) regardless of the length of the string. 
To that end, the class is ultimately composed of a tuple of string symbols, a magnitude, and up-to one conversion function.

**Instantiation:**
This class is built to be instantiated casually and intuitively, e.g. `Unit("m")`, so reasonable string inputs should be processed as expected.
That said, care should be taken to leave a space between symbols as milliseconds (`"ms"`) are quite different from meter seconds (`"m s"`).
Of-course, the class can also be instantiated more formally. Unit has three keywords for defining symbols: `numerators` and `denominators`, or `symbols`. 
These keywords accept tuples of string-units, e.g. `("m","s")`, or tuples of string-unit exponent tuple pairs, e.g. `( ("m",1), ("s",-1) )`. 
The keyword `magnitude` accepts numbers to define the magnitude of a unit. 

As an example, each of the following instantiated units have the same symbols

    Unit("m/s")
    Unit("m s^-1")
    Unit(numerators=("m",),denominators=("s",))
    Unit(numerators=(("m",1),),denominators=(("s",1),))
    Unit(symbols=(("m",1),("s",-1),))

As an example, each of the following instantiated units have the same magnitudes:

    Unit("1e6 fish")
    Unit("fish", magnitude=1e6)
    Unit("1000000 fish")
    Unit("10^6 fish")


**Context Dependent Units:**
Some function units, most notably the Decibel (dB), have a context dependent meaning; thus, the user is responsible for defining them prior to use.
In the case of the decibel , the function is `10*((val/ref).log10)` where `val` is value being measured and `ref` is the context dependent reference. 
More well-defined versions of the Decibels or Bels do exist, for example a milli-watt microbel (uBmW) is context independent and defined with respect to a milli-watt reference. 
These more well-defined units are considered obscure and non-metric (even when using a metric reference); thus, the user is responsible for defining them prior to use. 

### Defining Units

Generally, users do not need to define custom units. If a user wants to use some arbitrary unit such as `Unit("fish")`, the module is fully capable of managing that. 
It is also trivial to add magnitudes to arbitrary units (e.g. `Unit("10^6 fish")`), so some users may find it simpler to replace prefixes `.replace("Mfish","10^6 fish")`.
Moreover, the module has a number of predefined sets of non-standard units `Unit.IMPERIAL_UNITS`, `Unit.PRESSURE_UNITS`, `Unit.CONCENTRATION_UNITS` that can be loaded into the Unit or Measure class with an additional argument or the keywords `defs` or `definitions`.
Still, users may need to define custom units when dealing with non-standard derived units. Derived units must be defined to be converted to their base units. 

While not required, base units are commonly metric. This module considers metric base units to be units without a prefix. 
This is important any unit defined in terms of prefixed-metric-base units (i.e. kg's) may have unexpected behavior.
Additionally, this module does not infer prefiexs. If you define a unit that can be used with prefiexs, the prefixed unit must also be defined (It is trivial to do this in a loop).

Custom context dependent units are a rare case. In addition to the magnitude and base units, they require a user to define a selector function and at least two conversion functions. 
The selector function simply determines the behavior (the conversion functions used) given the exponent. The conversion functions are to and from base units. 

As an example, here are some metric units already included by default:

    def DEGREES_CELSIUS_SELECTOR(exponent):
      if(exponent == 0): return (lambda x:x,lambda x:x)
      # Degrees Celsius Functions
      def NUMERATOR_FORWARD_CELSIUS(val):
        val,abs_zero =val,Decimal("273.15")
        return val+abs_zero
      def NUMERATOR_REVERSE_CELSIUS(val):
        val,abs_zero = val,Decimal("273.15")
        return val-abs_zero
      def DENOMINATOR_FORWARD_CELSIUS(val):
        return val
      def DENOMINATOR_REVERSE_CELSIUS(val):
        return val
      # Select & Return Correct Function
      if(exponent == 1):  return (NUMERATOR_FORWARD_CELSIUS,NUMERATOR_REVERSE_CELSIUS)
      if(exponent == -1): return (DENOMINATOR_FORWARD_CELSIUS,DENOMINATOR_REVERSE_CELSIUS)
      else:
        raise AmbiguousUnitException(f"Failed to Decompose: Exponent of \u00B0C != 1,0,-1. Cannot Deconvolute.")
    weird_unit_dict = {
      # Symbol      Mult             Base-Symbol   Function                   Text          Dimension       
      'Hz'      : ( Decimal(1),      (('s',-1),),  None,                      'Hertz',      'Frequency'   ),
      'kHz'     : ( Decimal("1e3"),  (('s',-1),),  None,                      'kilohertz',  'Frequency'   ),
      "degC"    : ( Decimal(1),      (('K',1),),   DEGREES_CELSIUS_SELECTOR,  'Celsius',    'Temperature' ),
      }
    
    x = Measure("5 kHz",weird_unit_dict)

***If you make your a unit dictionary you'd like included in the package, please reach out to me.***

____________________________________________________________

# Frequently Asked Questions

## Can the module be used with NumPy/cmath? 

Yes, but the extra efficiency from NumPy is lost. 
If you're using the module for scripting purposes and are unconcerned about efficiency, simply use the argument `dtype=numpy.dtype(Measure)` in your NumPy array.
If you are creating a more high performance program, use this module to parser/convert your initial input into your preferred units, then take the value of measures (as floats if they aren't already).

Example:

    m = Measure("5 mm")
    a = numpy.array([m,m,m],dtype=numpy.dtype(Measure))


## What Types of numbers does it work with?

Thoroughly tested with Decimals, ints, floats. Might work with complex numbers from cmath, but not tested. 
It might not fail with other Numbers, but no guarantees. 


## Propagation (Domination) of the Measure class. 

When using the measure in maths you may find that most things convert to the measure class in the final result. 
Sometimes this makes sense, a scalar times a measure should be a measure. Other times this may seem annoying, as in unitless values. 
Unitless Measures are returned to help track the propagation of error. 
One can always access the value via the value property or by casting the measure as a float. 

## How does the module handle Celsius and Fahrenheit?

Just like every other unit, Celsius and Fahrenheit are decomposed (into Kelvin) prior to any math being done. 
Most unit managers do not do this because it is difficult to code addition into conversion functions. 
This module manages the difficult part; however, certain non-base units are invalid because they cannot be decomposed: e.g. `Measure("10 degC m")` will throw an error.
The reason is the module cannot know what portion of the unit belongs to each component: e.g. `Measure("2 m") * Measure("5 degC") != Measure("5 m") * Measure("2 degC")`.
Notice the module doesn't fail calculating `Measure("2 m") * Measure("5 degC")`. It simply doesn't back-convert to Celsius.
Note: The unit "C" is reserved for Coulomb, but the module recognizes the degrees symbol. 

## Conversions to Non-Metric Units: E.g. Feet(ft) to Inches(in)?

One common gripe about the `convert` function is that it doesn't propagate unit definitions. 
This results in situations where a conversion of inches to feet might be interpreted as an attempt to convert inches to femto-tonnes, resulting in an error: `Measure("12 in",Unit.IMPERIAL_UNITS).convert("ft")` throws a UnitException for incompatible units.
The proper way to convert to any non-metric unit is to define the unit in either convert or the passed unit: `Measure("12 in",Unit.IMPERIAL_UNITS).convert("ft",Unit.IMPERIAL_UNITS)` or `Measure("12 in",Unit.IMPERIAL_UNITS).convert(Unit("ft",Unit.IMPERIAL_UNITS))`.

# Less Frequently Asked Questions

## Can the module be made Faster?

One thing you can do to improve speed is to decompose units or simplify measures as early as possible.
The Decompose, Convert, and Simplify functions remove unit definitions, and propagation of unit-definitions slows the module.
This is not an issue for purely metric units because they are the default (thus never passed in propagation). 
The notable down side in removing the unit definitions is that you'll have to re-introduce the definitions if you intend to use them later. 

