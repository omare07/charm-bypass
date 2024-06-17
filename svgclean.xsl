<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:svg="http://www.w3.org/2000/svg"
		version="1.0">
  <xsl:output method="xml" encoding="UTF-8" />

  <!--
    This empty template for the xml:space attribute removes it from
    any element where it is found. Inkscape adds it automatically, but
    we don't rely on it, and it's been deprecated for a while:

      https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/xml:space

  -->
  <xsl:template match="@xml:space" />

  <!--
    This rule replaces a <tspan> directly inside of a <text> with its
    contents. The "directly" part is important because we actually use
    tspans in one place, for the origin -> destination. We don't want
    to clobber THOSE tspans, but we can avoid it by putting them in a
    group (<g>).
  -->
  <xsl:template match="svg:text/svg:tspan">
    <xsl:value-of select="text()" />
  </xsl:template>

  <!--
    Then this rule matches everything, and copies it while applying
    any relevant templates to its children. Either we'll hit a <tspan>
    within a <text> and process it, or we'll hit this rule again.
  -->
  <xsl:template match="node()|@*">
    <xsl:copy>
      <xsl:apply-templates select="node()|@*" />
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
