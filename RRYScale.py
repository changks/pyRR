from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms

class RRYScale(mscale.ScaleBase):
    """
    Scales data in range 1 to 99.9 using the below function:

    The scale function:
      y' = log10(log10(100/y))

    The inverse scale function:
      y = 100/(10**(10**y'))

    source:
    ACPS Mograph Series Volume 1 (pg 46)
    """

    # The scale class must have a member ``name`` that defines the
    # string used to select the scale.  For example,
    # ``gca().set_yscale("RRy")`` would be used to select this
    # scale.
    name = 'rry'

    def __init__(self, axis, **kwargs):
        """
        Any keyword arguments passed to ``set_xscale`` and
        ``set_yscale`` will be passed along to the scale's
        constructor.

        thresh: The degree above which to crop the data.
        """
        mscale.ScaleBase.__init__(self)
        thresh = kwargs.pop("thresh", 1.0)
        self.thresh = thresh

    def get_transform(self):
        """
        Override this method to return a new instance that does the
        actual transformation of the data.

        The RRYTransform class is defined below as a
        nested class of this one.
        """
        return self.RRYTransform(self.thresh)

    def set_default_locators_and_formatters(self, axis):
        """
        Override to set up the locators and formatters to use with the
        scale.  This is only required if the scale requires custom
        locators and formatters.  Writing custom locators and
        formatters is rather outside the scope of this example, but
        there are many helpful examples in ``ticker.py``.
        """

        axis.set_major_locator(mscale.FixedLocator(mscale.np.array([0.1, 1,5,10,20,30,40,50,60,70,75,80,85,90,92,94,96,98,99,99.5,99.8])))

    def limit_range_for_scale(self, vmin, vmax, minpos):
        """
        Override to limit the bounds of the axis to the domain of the
        transform.  In the case of Mercator, the bounds should be
        limited to the threshold that was passed in.  Unlike the
        autoscaling provided by the tick locators, this range limiting
        will always be adhered to, whether the axis range is set
        manually, determined automatically or changed through panning
        and zooming.
        """
        return max(vmin, 1), min(vmax, 100)

    class RRYTransform(mtransforms.Transform):
        # There are two value members that must be defined.
        # ``input_dims`` and ``output_dims`` specify number of input
        # dimensions and output dimensions to the transformation.
        # These are used by the transformation framework to do some
        # error checking and prevent incompatible transformations from
        # being connected together.  When defining transforms for a
        # scale, which are, by definition, separable and have only one
        # dimension, these members should always be set to 1.
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            """
            This transform takes an Nx1 ``numpy`` array and returns a
            transformed copy.  Since the range of the RR scale
            is limited by the user-specified threshold, the input
            array must be masked to contain only valid values.
            ``matplotlib`` will handle masked arrays and remove the
            out-of-range data from the plot.  Importantly, the
            ``transform`` method *must* return an array that is the
            same shape as the input array, since these values need to
            remain synchronized with values in the other dimension.
            """
            masked = mscale.ma.masked_where((a < self.thresh), a)
            if masked.mask.any():
                return mscale.ma.log10(mscale.ma.log10(100/masked))
            else:
                return mscale.np.log10(mscale.np.log10(100/a))

        def inverted(self):
            """
            Override this method so matplotlib knows how to get the
            inverse transform for this transform.
            """
            return RRYScale.InvertedRRYTransform(self.thresh)

    class InvertedRRYTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, thresh):
            mtransforms.Transform.__init__(self)
            self.thresh = thresh

        def transform(self, a):
            return 100/(10**(10**a))

        def inverted(self):
            return RRYScale.RRYTransform(self.thresh)