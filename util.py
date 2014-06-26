import matplotlib.pyplot as plt
import numpy as np


def hist2d(x,y,h, axes=None, **kwargs):
    """
    Draw a 2D matplotlib histogram plot from a 2D ROOT histogram.

    Parameters
    ----------

    h : Hist2D
        A rootpy Hist2D

    axes : matplotlib Axes instance, optional (default=None)
        The axes to plot on. If None then use the global current axes.

    kwargs : additional keyword arguments, optional
        Additional keyword arguments are passed directly to
        matplotlib's hist2d function.

    Returns
    -------

    Returns the value from matplotlib's hist2d function.

    """
    if axes is None:
        axes = plt.gca()
    X, Y = np.meshgrid(list(h.x()), list(h.y()))
    x = X.ravel()
    y = Y.ravel()
    z = np.array(h.z()).T
    axes.hist2d(x, y, weights=z.ravel(),
                       bins=(list(h.xedges()), list(h.yedges())),
                       **kwargs)

    return axes



def contour(x,y,h, axes=None, zoom=None, **kwargs):
    """
    Draw a matplotlib contour plot from a 2D ROOT histogram.

    Parameters
    ----------

    h : Hist2D
        A rootpy Hist2D

    axes : matplotlib Axes instance, optional (default=None)
        The axes to plot on. If None then use the global current axes.

    zoom : float or sequence, optional (default=None)
        The zoom factor along the axes. If a float, zoom is the same for each
        axis. If a sequence, zoom should contain one value for each axis.
        The histogram is zoomed using a cubic spline interpolation to create
        smooth contours.

    kwargs : additional keyword arguments, optional
        Additional keyword arguments are passed directly to
        matplotlib's contour function.

    Returns
    -------

    Returns the value from matplotlib's contour function.

    """
    if axes is None:
        axes = plt.gca()
    x = np.array(list(h.x()))
    y = np.array(list(h.y()))
    z = np.array(h.z()).T
    if zoom is not None:
        from scipy import ndimage
        if hasattr(zoom, '__iter__'):
            zoom = list(zoom)
            x = ndimage.zoom(x, zoom[0])
            y = ndimage.zoom(y, zoom[1])
        else:
            x = ndimage.zoom(x, zoom)
            y = ndimage.zoom(y, zoom)
        z = ndimage.zoom(z, zoom)
    axes.contour(x, y, z, **kwargs)
    return axes

# def bar(hists,
#         stacked=True,
#         reverse=False,
#         xerr=False, yerr=True,
#         xpadding=0, ypadding=.1,
#         yerror_in_padding=True,
#         rwidth=0.8,
#         snap=True,
#         axes=None,
#         **kwargs):
#     """
#     Make a matplotlib bar plot from a ROOT histogram, stack or
#     list of histograms.

#     Parameters
#     ----------

#     hists : Hist, list of Hist, HistStack
#         The histogram(s) to be plotted

#     stacked : bool or string, optional (default=True)
#         If True then stack the histograms with the first histogram on the
#         bottom, otherwise overlay them with the first histogram in the
#         background. If 'cluster', then the bars will be arranged side-by-side.

#     reverse : bool, optional (default=False)
#         If True then reverse the order of the stack or overlay.

#     xerr : bool, optional (default=False)
#         If True, x error bars will be displayed.

#     yerr : bool or string, optional (default=True)
#         If False, no y errors are displayed.  If True, an individual y
#         error will be displayed for each hist in the stack.  If 'linear' or
#         'quadratic', a single error bar will be displayed with either the
#         linear or quadratic sum of the individual errors.

#     xpadding : float or 2-tuple of floats, optional (default=0)
#         Padding to add on the left and right sides of the plot as a fraction of
#         the axes width after the padding has been added. Specify unique left
#         and right padding with a 2-tuple.

#     ypadding : float or 2-tuple of floats, optional (default=.1)
#         Padding to add on the top and bottom of the plot as a fraction of
#         the axes height after the padding has been added. Specify unique top
#         and bottom padding with a 2-tuple.

#     yerror_in_padding : bool, optional (default=True)
#         If True then make the padding inclusive of the y errors otherwise
#         only pad around the y values.

#     rwidth : float, optional (default=0.8)
#         The relative width of the bars as a fraction of the bin width.

#     snap : bool, optional (default=True)
#         If True (the default) then the origin is an implicit lower bound of the
#         histogram unless the histogram has both positive and negative bins.

#     axes : matplotlib Axes instance, optional (default=None)
#         The axes to plot on. If None then use the global current axes.

#     kwargs : additional keyword arguments, optional
#         All additional keyword arguments are passed to matplotlib's bar
#         function.

#     Returns
#     -------

#     The return value from matplotlib's bar function, or list of such return
#     values if a stack or list of histograms was plotted.

#     """
#     if axes is None:
#         axes = plt.gca()
#     curr_xlim = axes.get_xlim()
#     curr_ylim = axes.get_ylim()
#     was_empty = not axes.has_data()
#     logy = kwargs.pop('log', axes.get_yscale() == 'log')
#     kwargs['log'] = logy
#     returns = []
#     if isinstance(hists, _Hist):
#         # This is a single histogram.
#         returns = _bar(hists, xerr=xerr, yerr=yerr,
#                        axes=axes, **kwargs)
#         _set_bounds(hists, axes=axes,
#                     was_empty=was_empty,
#                     prev_xlim=curr_xlim,
#                     prev_ylim=curr_ylim,
#                     xpadding=xpadding, ypadding=ypadding,
#                     yerror_in_padding=yerror_in_padding,
#                     snap=snap,
#                     logy=logy)
#     elif stacked == 'cluster':
#         nhists = len(hists)
#         hlist = _maybe_reversed(hists, reverse)
#         for i, h in enumerate(hlist):
#             width = rwidth / nhists
#             offset = (1 - rwidth) / 2 + i * width
#             returns.append(_bar(
#                 h, offset, width,
#                 xerr=xerr, yerr=yerr, axes=axes, **kwargs))
#         _set_bounds(sum(hists), axes=axes,
#                     was_empty=was_empty,
#                     prev_xlim=curr_xlim,
#                     prev_ylim=curr_ylim,
#                     xpadding=xpadding, ypadding=ypadding,
#                     yerror_in_padding=yerror_in_padding,
#                     snap=snap,
#                     logy=logy)
#     elif stacked is True:
#         nhists = len(hists)
#         hlist = _maybe_reversed(hists, reverse)
#         toterr = bottom = None
#         if yerr == 'linear':
#             toterr = [sum([h.GetBinError(i) for h in hists])
#                       for i in range(1, hists[0].nbins(0) + 1)]
#         elif yerr == 'quadratic':
#             toterr = [sqrt(sum([h.GetBinError(i) ** 2 for h in hists]))
#                       for i in range(1, hists[0].nbins(0) + 1)]
#         for i, h in enumerate(hlist):
#             err = None
#             if yerr is True:
#                 err = True
#             elif yerr and i == (nhists - 1):
#                 err = toterr
#             returns.append(_bar(
#                 h,
#                 xerr=xerr, yerr=err,
#                 bottom=list(bottom.y()) if bottom else None,
#                 axes=axes, **kwargs))
#             if bottom is None:
#                 bottom = h.Clone()
#             else:
#                 bottom += h
#         _set_bounds(bottom, axes=axes,
#                     was_empty=was_empty,
#                     prev_xlim=curr_xlim,
#                     prev_ylim=curr_ylim,
#                     xpadding=xpadding, ypadding=ypadding,
#                     yerror_in_padding=yerror_in_padding,
#                     snap=snap,
#                     logy=logy)
#     else:
#         for h in hlist:
#             returns.append(_bar(h, xerr=xerr, yerr=yerr,
#                                 axes=axes, **kwargs))
#         _set_bounds(max(hists), axes=axes,
#                     was_empty=was_empty,
#                     prev_xlim=curr_xlim,
#                     prev_ylim=curr_ylim,
#                     xpadding=xpadding, ypadding=ypadding,
#                     yerror_in_padding=yerror_in_padding,
#                     snap=snap,
#                     logy=logy)
#     return axes
