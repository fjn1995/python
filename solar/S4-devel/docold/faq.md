% S4 Frequently Asked Questions
% Victor Liu (vkl@stanford.edu)
% Mar 30, 2013
<style type="text/css">
@import url(s4.css);
</style>

[S4 Home](index.html) | [Download](download.html) | [FAQ](faq.html) | [Lua API](s4_lua_api.html) | [Developer information](dev_info.html) | [Changelog](changelog.html)

# Frequently Asked Questions

* What are the units?

  S4 deals with only linear electromagnetism, so Maxwell's equations are
  scale invariant. This means that in some sense there are no units.
  To think of it a different way, you can decide that all length numbers
  correspond to microns, then frequency is in units of c/microns, where c
  is the speed of light, and so on.

* What is the coordinate system?

  All spatial coordinates are cartesian. They are not in terms of the
  lattice vector basis.

* Where is the unit cell located and do I need to define periodic copies of patterns?

  This a tricky topic. If you use an FMM formuation which is based on
  analytic Fourier transforms (which includes the default settings),
  then all patterns are automatically periodized, and in some sense,
  the shape and location of the unit cell is irrelevant. For spatially
  sampled FMM formulations (those that rely on an FFT), the unit cell
  is the Wigner-Seitz cell centered at the origin. For these formulations
  you need to specify periodic copies.
  
  You should always check that the patterning is specified correctly
  using GetEpsilon() or OutputLayerPatternRealization().
  
* What happens if I get a quantity "outside" the structure?

  For example, if you specify a negative z coordinate, that corresponds
  to being within the first layer, since it is assumed the first layer
  extends infinitely towards negative infinity in the z direction.
  Similarly, if you specify a z coordinate past the total thickness of
  all layers, it is within the last layer. This is why you can specify
  zero thickness for the first and last layers.

* How do I specify frequency dependent material parameters?

  If you have a loop iterating over frequencies, then within the loop
  simply set new epsilon values for the materials. In order to incorporate
  values from tabulated data, you can use the Interpolator object and
  pass it a table of values. Large tables can be defined in separate
  files and included using the Lua dofile() function.

* Why is the POVRay output wrong?

  The POVRay feature is only to provide a starting point for writing
  an actual POVRay script. It is not guaranteed to be correct. You
  should not rely on this feature.
