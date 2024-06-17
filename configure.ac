AC_PREREQ([2.71])
AC_INIT([charm-bypass],[0.0.1],[michael@orlitzky.com])
AC_CONFIG_AUX_DIR([build-aux])
AM_INIT_AUTOMAKE([-Wall foreign no-dist-gzip dist-xz tar-ustar])
AC_CONFIG_FILES([Makefile])
AC_CONFIG_SRCDIR([tableau.svg])

AC_PATH_PROG([BASE64], [base64])
AS_IF(
  [test -z "${BASE64}"],
  [AC_MSG_ERROR([base64 program not found])]
)

AC_PATH_PROG([FONTFORGE], [fontforge])
AS_IF(
  [test -z "${FONTFORGE}"],
  [AC_MSG_ERROR([fontforge program not found])]
)

AC_PATH_PROG([SCOUR], [scour])
AS_IF(
  [test -z "${SCOUR}"],
  [AC_MSG_ERROR([scour program not found])]
)

AC_PATH_PROG([XSLTPROC], [xsltproc])
AS_IF(
  [test -z "${XSLTPROC}"],
  [AC_MSG_ERROR([xsltproc program not found])]
)

AC_OUTPUT
