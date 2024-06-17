#!/bin/sh
#
# A posix sh CGI script (yeah, that's right) to update the daily
# code for CharmBypass. This is not useful to you unless you
# host CharmBypass on a public web server and are insane.
#

# Fail on the first error.
set -e

# The CGI spec says that the current working directory SHOULD be set
# to the directory containing the script. Well, that's not always what
# happens. It's true in apache...
INDEX_HTML=$(pwd)/../index.html

# But not in python's server.http
[ -f "${INDEX_HTML}" ] || INDEX_HTML=$(pwd)/index.html


# Die with an error. The first argument, an HTTP status code, is
# returned as the Status. The second argument, an error message, is
# printed after setting the Content-type to text/plain. Finally, we
# cease execution.
die() {
  echo "Status: ${1}"
  echo "Content-type: text/plain"
  echo ""
  echo "${2}"
  exit 1
}

# Redirect to the given URL; return a 302 status, and send the
# necessary location header.
redirect() {
  echo "Status: 302"
  echo "Location: ${1}"
  echo ""
  exit
}

# Parse and return the daily code from the index.html file.
# This relies on "implementation details" within the HTML;
# namely, the field name and its value must appear next
# to each other on the same line.
parse_code() {
  sed -n \
      -e 's/.*name="code" value="\([A-Za-z0-9]\{2\}\)".*/\1/p' \
      "${INDEX_HTML}" \
      | head -n 1
}

# Update (replace) the daily code in the index.html file. The first
# argument is the new code to use. This relies on "implementation
# details" within the HTML; namely, the field name and its value must
# appear next to each other on the same line.
update_code() {
  _new_code="${1}"
  _find='name="code" value="[a-zA-Z0-9]\{0,2\}"'
  _replace="name=\"code\" value=\"${_new_code}\""
  _tmp=$(mktemp)

  # The "-i" flag to sed isn't POSIX, and worse, it tries to use a
  # temp file in CWD. We don't want to make the parent directory
  # writable because then this script is writable.
  sed -e "s/${_find}/${_replace}/g" "${INDEX_HTML}" > "${_tmp}"

  # mv would also recreate the file here, so cp/rm instead.
  cp "${_tmp}" "${INDEX_HTML}"
  rm "${_tmp}"
}

# Display the "update code" form and exit.
display_code_form() {
  echo "Content-type: text/html"
  echo ""

  cat <<-EOF
	<!doctype html>
	<html lang="en-US">
	  <head>
	    <meta charset="utf-8">
	    <meta name="viewport"
	          content="width=device-width, initial-scale=1" />

	    <title>
	      CharmBypass: got that transit equity
	    </title>
	  </head>

	  <body>
	    <form method="post">
	      <label for="code">Today's code:</label>
	      <input id="code"
	             name="code" value="${1}"
	             type="text"
	             size="2"
	             minlength="2"
	             maxlength="2"
	             pattern="[a-zA-Z0-9]*" />
	      <br /><br />
	      <input type="submit" value="Update it" />
	    <form>
	  </body>
	</html>
EOF
  exit
}

# If this isn't a POST request, it should be a "normal" page hit,
# i.e. a GET request with no querystring parameters. If there are
# parameters, we ignore them, and display the "update code" form
# anyway.
if [ "${REQUEST_METHOD}" != "POST" ]; then
  # Parse the code before we start displaying the form
  # so that we can throw a 500 error if it fails.
  _old_code=$(parse_code) || die 500 "failed to parse the existing code"
  display_code_form "${_old_code}"
fi

# Since display_code_form() exits, the only way we can get
# here is if this is a POST request. And in that case, we
# should have some data... At least, CONTENT_LENGTH will
# be a number.
if [ -n "${CONTENT_LENGTH}" -a "${CONTENT_LENGTH}" -gt 0 ]; then
  POST_DATA=$(dd bs=1 count="${CONTENT_LENGTH}" 2>/dev/null)

  # Sanity check the form data. To prevent mistakes, it's not possible
  # to "erase" the code that somebody else entered. If it's wrong, who
  # cares? Erasing it would make it random... i.e. still wrong.
  case "${POST_DATA}" in
    "code="[A-Za-z0-9][A-Za-z0-9])
	CODE=$(echo "${POST_DATA}" | cut -d= -f2)
	update_code "${CODE}" || die 500 "failed to update the code"
	redirect "/"
	;;
    *)
      # If the form data isn't exactly what we expect,
      # fail ASAP.
      die 400 "bad request"
      ;;
  esac
fi
