# If you really want to, we support installing index.html
# to (say) /usr/share/charm-bypass/index.html
dist_pkgdata_DATA = index.html

# A single POSIX shell script is our "test suite."
TESTS = run-tests.sh

# Based on e.g.
#
#   https://www.gnu.org/software/automake/manual/html_node/Scripts.html
#
# this looks like the best way to include "sources" for things that
# aren't true programs/libraries.
EXTRA_DIST =              \
  $(TESTS)                \
  CharmBypass-Regular.sfd \
  CharmBypass-Bold.sfd    \
  favicon.svg             \
  index.html.in           \
  sfd2woff.ff             \
  svgclean.xsl            \
  tableau.svg

# List of element IDs that we use in the HTML document.
PRECIOUS_IDS = \
  bus          \
  city         \
  citycopy     \
  codebg       \
  codetext     \
  clouds       \
  cloudscopy   \
  destination  \
  origin       \
  origindest   \
  train        \
  tram         \
  trees        \
  treescopy    \
  serviceid    \
  servicename  \
  sky          \
  ticket       \
  ticketbg     \
  ticketdate   \
  tickettime   \
  zone

# The base "scour" command used to optimize the tableau and favicon.
SCOUR = @SCOUR@                 \
  --enable-id-stripping         \
  --enable-comment-stripping    \
  --remove-descriptive-elements \
  --no-renderer-workaround      \
  --no-line-breaks              \
  --error-on-flowtext

# Optimize the favicon using scour.
favicon.min.svg: favicon.svg
	$(SCOUR) $< > $@

# Optimize the tableau once using XSL, to catch a few things that
# "scour" will miss...
tableau.min.svg: tableau.svg svgclean.xsl
	@XSLTPROC@ $(srcdir)/svgclean.xsl $< > $@

# Optimize the tableau (again) using scour, removing its XML prologue
# so that it can be included directly into the HTML document.
tableau.min.min.svg: tableau.min.svg
	$(SCOUR) --protect-ids-list=$$(echo $(PRECIOUS_IDS) | tr ' ' ',') \
                 --strip-xml-prolog \
                 $< > $@

# Use FontForge to convert the sfd source files to woff2.
.sfd.woff2:
	@FONTFORGE@ -script $(srcdir)/sfd2woff.ff $< $@

# Base64-encode a woff2 (web open font format 2.0) file. We use this
# to embed fonts directly into the CSS that requires them.
.woff2.gbase64:
	@BASE64@ -w0 $< > $@

# Same with the favicon SVG.
.svg.gbase64:
	@BASE64@ -w0 $< > $@

# List all of the dependencies of the final index.html that themselves
# had to be built. We collect them here because they need to be listed
# in two places, as dependencies of index.html, and in CLEANFILES.
index_html_BUILTDEPS = \
  CharmBypass-Regular.gbase64 \
  CharmBypass-Bold.gbase64    \
  favicon.gbase64             \
  tableau.min.min.svg

# Build index.html by substituting the contents of a few (single
# line!) files into @PLACEHOLDERS@ within index.html.in. If you put
# tildes in tableau.svg this will break, so please don't do that.
index.html: index.html.in $(index_html_BUILTDEPS)
	sed -e "s~@CBPREGULAR@~$$(cat CharmBypass-Regular.gbase64)~" \
            -e "s~@CBPBOLD@~$$(cat CharmBypass-Bold.gbase64)~" \
            -e "s~@FAVICON@~$$(cat favicon.gbase64)~" \
            -e "s~@SVGDATA@~$$(cat tableau.min.min.svg)~" \
            $< > $@

# Automake doesn't understand our wacky build process so we have to
# tell it which files are produced by running "make".
CLEANFILES =              \
  $(dist_pkgdata_DATA)    \
  $(index_html_BUILTDEPS) \
  favicon.min.svg         \
  tableau.min.svg

