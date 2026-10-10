Bumps the python-deps group with 8 updates:

| Package | From | To |
| --- | --- | --- |
| [flask](https://github.com/pallets/flask) | `2.2.5` | `3.1.3` |
| [werkzeug](https://github.com/pallets/werkzeug) | `2.2.3` | `3.1.9` |
| [jinja2](https://github.com/pallets/jinja) | `3.1.2` | `3.1.6` |
| [click](https://github.com/pallets/click) | `8.1.3` | `8.5.0` |
| [requests](https://github.com/psf/requests) | `2.31.0` | `2.34.2` |
| [urllib3](https://github.com/urllib3/urllib3) | `1.26.18` | `2.8.0` |
| [pyyaml](https://github.com/yaml/pyyaml) | `6.0.1` | `6.0.3` |
| [pytest](https://github.com/pytest-dev/pytest) | `7.4.0` | `9.1.1` |

Updates `flask` from 2.2.5 to 3.1.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/pallets/flask/releases">flask's releases</a>.</em></p>
<blockquote>
<h2>3.1.3</h2>
<p>This is the Flask 3.1.3 security fix release, which fixes a security issue but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Flask/3.1.3/">https://pypi.org/project/Flask/3.1.3/</a>
Changes: <a href="https://flask.palletsprojects.com/page/changes/#version-3-1-3">https://flask.palletsprojects.com/page/changes/#version-3-1-3</a></p>
<ul>
<li>The session is marked as accessed for operations that only access the keys but not the values, such as <code>in</code> and <code>len</code>. <a href="https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726">GHSA-68rp-wp8r-4726</a></li>
</ul>
<h2>3.1.2</h2>
<p>This is the Flask 3.1.2 fix release, which fixes bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Flask/3.1.2/">https://pypi.org/project/Flask/3.1.2/</a>
Changes: <a href="https://flask.palletsprojects.com/page/changes/#version-3-1-2">https://flask.palletsprojects.com/page/changes/#version-3-1-2</a>
Milestone: <a href="https://github.com/pallets/flask/milestone/38?closed=1">https://github.com/pallets/flask/milestone/38?closed=1</a></p>
<ul>
<li><code>stream_with_context</code> does not fail inside async views. <a href="https://redirect.github.com/pallets/flask/issues/5774">#5774</a></li>
<li>When using <code>follow_redirects</code> in the test client, the final state of <code>session</code> is correct. <a href="https://redirect.github.com/pallets/flask/issues/5786">#5786</a></li>
<li>Relax type hint for passing bytes IO to <code>send_file</code>. <a href="https://redirect.github.com/pallets/flask/issues/5776">#5776</a></li>
</ul>
<h2>3.1.1</h2>
<p>This is the Flask 3.1.1 fix release, which fixes bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Flask/3.1.1/">https://pypi.org/project/Flask/3.1.1/</a>
Changes: <a href="https://flask.palletsprojects.com/en/stable/changes/#version-3-1-1">https://flask.palletsprojects.com/en/stable/changes/#version-3-1-1</a>
Milestone <a href="https://github.com/pallets/flask/milestone/36?closed=1">https://github.com/pallets/flask/milestone/36?closed=1</a></p>
<ul>
<li>Fix signing key selection order when key rotation is enabled via <code>SECRET_KEY_FALLBACKS</code>. GHSA-4grg-w6v8-c28g</li>
<li>Fix type hint for <code>cli_runner.invoke</code>. <a href="https://redirect.github.com/pallets/flask/issues/5645">#5645</a></li>
<li><code>flask --help</code> loads the app and plugins first to make sure all commands are shown. <a href="https://redirect.github.com/pallets/flask/issues/5673">#5673</a></li>
<li>Mark sans-io base class as being able to handle views that return <code>AsyncIterable</code>. This is not accurate for Flask, but makes typing easier for Quart. <a href="https://redirect.github.com/pallets/flask/issues/5659">#5659</a></li>
</ul>
<h2>3.1.0</h2>
<p>This is the Flask 3.1.0 feature release. A feature release may include new features, remove previously deprecated code, add new deprecations, or introduce potentially breaking changes. We encourage everyone to upgrade, and to use a tool such as <a href="https://pypi.org/project/pip-tools/">pip-tools</a> to pin all dependencies and control upgrades. Test with warnings treated as errors to be able to adapt to deprecation warnings early.</p>
<p>PyPI: <a href="https://pypi.org/project/Flask/3.1.0/">https://pypi.org/project/Flask/3.1.0/</a>
Changes: <a href="https://flask.palletsprojects.com/en/stable/changes/#version-3-1-0">https://flask.palletsprojects.com/en/stable/changes/#version-3-1-0</a>
Milestone: <a href="https://github.com/pallets/flask/milestone/33?closed=1">https://github.com/pallets/flask/milestone/33?closed=1</a></p>
<ul>
<li>Drop support for Python 3.8. <a href="https://redirect.github.com/pallets/flask/issues/5623">#5623</a></li>
<li>Update minimum dependency versions to latest feature releases. Werkzeug &gt;= 3.1, ItsDangerous &gt;= 2.2, Blinker &gt;= 1.9. <a href="https://redirect.github.com/pallets/flask/issues/5624">#5624</a>, <a href="https://redirect.github.com/pallets/flask/issues/5633">#5633</a></li>
<li>Provide a configuration option to control automatic option responses. <a href="https://redirect.github.com/pallets/flask/issues/5496">#5496</a></li>
<li><code>Flask.open_resource</code>/<code>open_instance_resource</code> and <code>Blueprint.open_resource</code> take an <code>encoding</code> parameter to use when opening in text mode. It defaults to <code>utf-8</code>. <a href="https://redirect.github.com/pallets/flask/issues/5504">#5504</a></li>
<li><code>Request.max_content_length</code> can be customized per-request instead of only through the <code>MAX_CONTENT_LENGTH</code> config. Added <code>MAX_FORM_MEMORY_SIZE</code> and <code>MAX_FORM_PARTS</code> config. Added documentation about resource limits to the security page. <a href="https://redirect.github.com/pallets/flask/issues/5625">#5625</a></li>
<li>Add support for the <code>Partitioned</code> cookie attribute (CHIPS), with the <code>SESSION_COOKIE_PARTITIONED</code> config. <a href="https://redirect.github.com/pallets/flask/issues/5472">#5472</a></li>
<li><code>-e path</code> takes precedence over default <code>.env</code> and <code>.flaskenv</code> files. <code>load_dotenv</code> loads default files in addition to a path unless <code>load_defaults=False</code> is passed. <a href="https://redirect.github.com/pallets/flask/issues/5628">#5628</a></li>
<li>Support key rotation with the <code>SECRET_KEY_FALLBACKS</code> config, a list of old secret keys that can still be used for unsigning. Extensions will need to add support. <a href="https://redirect.github.com/pallets/flask/issues/5621">#5621</a></li>
<li>Fix how setting <code>host_matching=True</code> or <code>subdomain_matching=False</code> interacts with <code>SERVER_NAME</code>. Setting <code>SERVER_NAME</code> no longer restricts requests to only that domain. <a href="https://redirect.github.com/pallets/flask/issues/5553">#5553</a></li>
<li><code>Request.trusted_hosts</code> is checked during routing, and can be set through the <code>TRUSTED_HOSTS</code> config. <a href="https://redirect.github.com/pallets/flask/issues/5636">#5636</a></li>
</ul>
<h2>3.0.3</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pallets/flask/blob/main/CHANGES.rst">flask's changelog</a>.</em></p>
<blockquote>
<h2>Version 3.1.3</h2>
<p>Released 2026-02-18</p>
<ul>
<li>The session is marked as accessed for operations that only access the keys
but not the values, such as <code>in</code> and <code>len</code>. :ghsa:<code>68rp-wp8r-4726</code></li>
</ul>
<h2>Version 3.1.2</h2>
<p>Released 2025-08-19</p>
<ul>
<li><code>stream_with_context</code> does not fail inside async views. :issue:<code>5774</code></li>
<li>When using <code>follow_redirects</code> in the test client, the final state
of <code>session</code> is correct. :issue:<code>5786</code></li>
<li>Relax type hint for passing bytes IO to <code>send_file</code>. :issue:<code>5776</code></li>
</ul>
<h2>Version 3.1.1</h2>
<p>Released 2025-05-13</p>
<ul>
<li>Fix signing key selection order when key rotation is enabled via
<code>SECRET_KEY_FALLBACKS</code>. :ghsa:<code>4grg-w6v8-c28g</code></li>
<li>Fix type hint for <code>cli_runner.invoke</code>. :issue:<code>5645</code></li>
<li><code>flask --help</code> loads the app and plugins first to make sure all commands
are shown. :issue:<code>5673</code></li>
<li>Mark sans-io base class as being able to handle views that return
<code>AsyncIterable</code>. This is not accurate for Flask, but makes typing easier
for Quart. :pr:<code>5659</code></li>
</ul>
<h2>Version 3.1.0</h2>
<p>Released 2024-11-13</p>
<ul>
<li>Drop support for Python 3.8. :pr:<code>5623</code></li>
<li>Update minimum dependency versions to latest feature releases.
Werkzeug &gt;= 3.1, ItsDangerous &gt;= 2.2, Blinker &gt;= 1.9. :pr:<code>5624,5633</code></li>
<li>Provide a configuration option to control automatic option
responses. :pr:<code>5496</code></li>
<li><code>Flask.open_resource</code>/<code>open_instance_resource</code> and
<code>Blueprint.open_resource</code> take an <code>encoding</code> parameter to use when
opening in text mode. It defaults to <code>utf-8</code>. :issue:<code>5504</code></li>
<li><code>Request.max_content_length</code> can be customized per-request instead of only
through the <code>MAX_CONTENT_LENGTH</code> config. Added</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pallets/flask/commit/22d924701a6ae2e4cd01e9a15bbaf3946094af65"><code>22d9247</code></a> release version 3.1.3</li>
<li><a href="https://github.com/pallets/flask/commit/089cb86dd22bff589a4eafb7ab8e42dc357623b4"><code>089cb86</code></a> Merge commit from fork</li>
<li><a href="https://github.com/pallets/flask/commit/c17f379390731543eea33a570a47bd4ef76a54fa"><code>c17f379</code></a> request context tracks session access</li>
<li><a href="https://github.com/pallets/flask/commit/27be9338405382445a7cb01151e084559b98d602"><code>27be933</code></a> start version 3.1.3</li>
<li><a href="https://github.com/pallets/flask/commit/4e652d3f68b90d50aa2301d3b7e68c3fafd9251d"><code>4e652d3</code></a> Abort if the instance folder cannot be created (<a href="https://redirect.github.com/pallets/flask/issues/5903">#5903</a>)</li>
<li><a href="https://github.com/pallets/flask/commit/3d03098a97ddc6a908aa4a50c2ef7381f8297d0a"><code>3d03098</code></a> Abort if the instance folder cannot be created</li>
<li><a href="https://github.com/pallets/flask/commit/407eb76b27884848383a37c7274654f0271e4bc4"><code>407eb76</code></a> document using gevent for async (<a href="https://redirect.github.com/pallets/flask/issues/5900">#5900</a>)</li>
<li><a href="https://github.com/pallets/flask/commit/ac5664d2281533eacafd64f5cc7d5edcdaccab60"><code>ac5664d</code></a> document using gevent for async</li>
<li><a href="https://github.com/pallets/flask/commit/4f79d5b59a56bc4356a97f2e81a35f98cb18d7b3"><code>4f79d5b</code></a> Increase required flit_core version to 3.11 (<a href="https://redirect.github.com/pallets/flask/issues/5865">#5865</a>)</li>
<li><a href="https://github.com/pallets/flask/commit/fe3b215d3ade4db68262dae1a3cdc464a1fc524f"><code>fe3b215</code></a> Increase required flit_core version to 3.11</li>
<li>Additional commits viewable in <a href="https://github.com/pallets/flask/compare/2.2.5...3.1.3">compare view</a></li>
</ul>
</details>
<br />

Updates `werkzeug` from 2.2.3 to 3.1.9
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/pallets/werkzeug/releases">werkzeug's releases</a>.</em></p>
<blockquote>
<h2>3.1.9</h2>
<p>This is the Werkzeug 3.1.9 security fix release, which fixes security issues and bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Werkzeug/3.1.9/">https://pypi.org/project/Werkzeug/3.1.9/</a>
Changes: <a href="https://werkzeug.palletsprojects.com/page/changes/#version-3-1-9">https://werkzeug.palletsprojects.com/page/changes/#version-3-1-9</a>
Milestone: <a href="https://github.com/pallets/werkzeug/milestone/46?closed=1">https://github.com/pallets/werkzeug/milestone/46?closed=1</a></p>
<ul>
<li><code>safe_join</code> on Windows does not allow special devices names with empty ADS markers on NTFS. <a href="https://github.com/pallets/werkzeug/security/advisories/GHSA-g6x2-hccm-hh4m">https://github.com/pallets/werkzeug/security/advisories/GHSA-g6x2-hccm-hh4m</a></li>
<li><code>ProfilerMiddleware</code> uses <code>profiling.tracing</code> on Python 3.15. <a href="https://redirect.github.com/pallets/werkzeug/issues/3207">#3207</a></li>
<li><code>uri_to_iri</code> and <code>iri_to_uri</code> preserve empty username, password, and port 0. <a href="https://redirect.github.com/pallets/werkzeug/issues/3189">#3189</a></li>
<li>Improve performance of <code>parse_options_header</code>. <a href="https://redirect.github.com/pallets/werkzeug/issues/3231">#3231</a></li>
<li>Improve performance of <code>parse_etags</code>. <a href="https://redirect.github.com/pallets/werkzeug/issues/3231">#3231</a></li>
<li>Improve performance of <code>parse_cookie</code>. <a href="https://redirect.github.com/pallets/werkzeug/issues/3231">#3231</a></li>
<li><code>get_host</code> also checks that the port is in the valid range. <a href="https://redirect.github.com/pallets/werkzeug/issues/3236">#3236</a></li>
<li>The <code>int</code> URL converter returns a 404 instead of 500 error when the value is longer than <code>sys.get_int_max_str_digits()</code>. <a href="https://redirect.github.com/pallets/werkzeug/issues/3237">#3237</a></li>
<li>Improve debugger PIN generation from cgroup data inside Podman. <a href="https://redirect.github.com/pallets/werkzeug/issues/3245">#3245</a></li>
<li><code>Authorization</code> parsing <code>basic</code> auth disallows non-base64 characters.  <a href="https://redirect.github.com/pallets/werkzeug/issues/3248">#3248</a></li>
<li><code>application/x-www-form-urlencoded</code> form data is no longer limited to <code>max_form_memory_size</code>, only <code>max_content_length</code>. <a href="https://redirect.github.com/pallets/werkzeug/issues/3251">#3251</a></li>
<li><code>LimitedStream.readinto</code> does not resize the buffer when it reads less than the remaining size. <a href="https://redirect.github.com/pallets/werkzeug/issues/3253">#3253</a></li>
<li>Rules with 10 or more converters in a single part assign matched values correctly. <a href="https://redirect.github.com/pallets/werkzeug/issues/3254">#3254</a></li>
<li>The invalid <code>Range</code> suffix length <code>-0</code> is no longer accepted. <a href="https://redirect.github.com/pallets/werkzeug/issues/3255">#3255</a></li>
</ul>
<h2>3.1.8</h2>
<p>This is the Werkzeug 3.1.8 fix release, which fixes bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Werkzeug/3.1.8/">https://pypi.org/project/Werkzeug/3.1.8/</a>
Changes: <a href="https://werkzeug.palletsprojects.com/page/changes/#version-3-1-8">https://werkzeug.palletsprojects.com/page/changes/#version-3-1-8</a>
Milestone: <a href="https://github.com/pallets/werkzeug/milestone/45?closed=1">https://github.com/pallets/werkzeug/milestone/45?closed=1</a></p>
<ul>
<li><code>Request.host</code> and <code>get_host</code> return the empty string if the header is missing or has invalid characters. <a href="https://redirect.github.com/pallets/werkzeug/issues/3142">#3142</a></li>
</ul>
<h2>3.1.7</h2>
<p>This is the Werkzeug 3.1.7 fix release, which fixes bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Werkzeug/3.1.7/">https://pypi.org/project/Werkzeug/3.1.7/</a>
Changes: <a href="https://werkzeug.palletsprojects.com/page/changes/#version-3-1-7">https://werkzeug.palletsprojects.com/page/changes/#version-3-1-7</a>
Milestone: <a href="https://github.com/pallets/werkzeug/milestone/44?closed=1">https://github.com/pallets/werkzeug/milestone/44?closed=1</a></p>
<ul>
<li><code>parse_list_header</code> preserves partially quoted items, discards empty items, and returns empty for unclosed quoted values. <a href="https://redirect.github.com/pallets/werkzeug/issues/3128">#3128</a></li>
<li><code>WWWAuthenticate.to_header</code> does not produce a trailing space when there are no parameters. <a href="https://redirect.github.com/pallets/werkzeug/issues/3127">#3127</a></li>
<li><code>Transfer-Encoding</code> is parsed as a set. <a href="https://redirect.github.com/pallets/werkzeug/issues/3134">#3134</a></li>
<li><code>Request.host</code>, <code>get_host</code>, and <code>host_is_trusted</code> validate the characters of the value. An empty value is no longer allowed. A Unix socket server address is ignored. The <code>trusted_list</code> argument to <code>host_is_trusted</code> is optional. <a href="https://redirect.github.com/pallets/werkzeug/issues/3113">#3113</a></li>
<li>Fix multipart form parser handling of newline at boundary. <a href="https://redirect.github.com/pallets/werkzeug/issues/3088">#3088</a></li>
<li><code>Response.make_conditional</code> sets the <code>Accept-Ranges</code> header even if it is not a satisfiable range request. <a href="https://redirect.github.com/pallets/werkzeug/issues/3108">#3108</a></li>
<li><code>merge_slashes</code> merges any number of consecutive slashes. <a href="https://redirect.github.com/pallets/werkzeug/issues/3121">#3121</a></li>
</ul>
<h2>3.1.6</h2>
<p>This is the Werkzeug 3.1.6 security fix release, which fixes a security issue but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Werkzeug/3.1.6/">https://pypi.org/project/Werkzeug/3.1.6/</a></p>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pallets/werkzeug/blob/main/CHANGES.rst">werkzeug's changelog</a>.</em></p>
<blockquote>
<h2>Version 3.1.9</h2>
<p>Released 2026-09-27</p>
<ul>
<li><code>safe_join</code> on Windows does not allow special devices names with empty ADS
markers on NTFS. :ghsa:<code>g6x2-hccm-hh4m</code></li>
<li><code>ProfilerMiddleware</code> uses <code>profiling.tracing</code> on Python 3.15.
:issue:<code>3207</code></li>
<li><code>uri_to_iri</code> and <code>iri_to_uri</code> preserve empty username, password, and
port 0. :issue:<code>3189</code></li>
<li>Improve performance of <code>parse_options_header</code>. :pr:<code>3231</code></li>
<li>Improve performance of <code>parse_etags</code>. :pr:<code>3231</code></li>
<li>Improve performance of <code>parse_cookie</code>. :pr:<code>3231</code></li>
<li><code>get_host</code> also checks that the port is in the valid range. :pr:<code>3236</code></li>
<li>The <code>int</code> URL converter returns a 404 instead of 500 error when the value
is longer than <code>sys.get_int_max_str_digits()</code>. :issue:<code>3237</code></li>
<li>Improve debugger PIN generation from cgroup data inside Podman.
:issue:<code>3245</code></li>
<li><code>Authorization</code> parsing <code>basic</code> auth disallows non-base64 characters.
:pr:<code>3248</code></li>
<li><code>application/x-www-form-urlencoded</code> form data is no longer limited to
<code>max_form_memory_size</code>, only <code>max_content_length</code>. :pr:<code>3251</code></li>
<li><code>LimitedStream.readinto</code> does not resize the buffer when it reads less
than the remaining size. :pr:<code>3253</code></li>
<li>Rules with 10 or more converters in a single part assign matched values
correctly. :pr:<code>3254</code></li>
<li>The invalid <code>Range</code> suffix length <code>-0</code> is no longer accepted. :pr:<code>3255</code></li>
</ul>
<h2>Version 3.1.8</h2>
<p>Released 2026-04-02</p>
<ul>
<li><code>Request.host</code> and <code>get_host</code> return the empty string if the header is
missing or has invalid characters. :issue:<code>3142</code></li>
</ul>
<h2>Version 3.1.7</h2>
<p>Released 2026-03-23</p>
<ul>
<li><code>parse_list_header</code> preserves partially quoted items, discards empty
items, and returns empty for unclosed quoted values. :pr:<code>3128</code></li>
<li><code>WWWAuthenticate.to_header</code> does not produce a trailing space when there
are no parameters. :issue:<code>3127</code></li>
<li><code>Transfer-Encoding</code> is parsed as a set. :pr:<code>3134</code></li>
<li><code>Request.host</code>, <code>get_host</code>, and <code>host_is_trusted</code> validate the</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pallets/werkzeug/commit/6604c3b8784ecc7cf5ac0b7412d916989b4c7d45"><code>6604c3b</code></a> release version 3.1.9</li>
<li><a href="https://github.com/pallets/werkzeug/commit/a78b30ac0cafe53a4f252ffbf827bf6da7591341"><code>a78b30a</code></a> update dependencies</li>
<li><a href="https://github.com/pallets/werkzeug/commit/8d77320bcdf3a34941ec06dcf16b03c065cd21b6"><code>8d77320</code></a> disallow special name with ads (<a href="https://redirect.github.com/pallets/werkzeug/issues/3309">#3309</a>)</li>
<li><a href="https://github.com/pallets/werkzeug/commit/b2a2c09730086ab2d375f0b069c821d4edf526b7"><code>b2a2c09</code></a> disallow special name with ads</li>
<li><a href="https://github.com/pallets/werkzeug/commit/4efac9df7ebabe13f82ab0823d5ca0109db20bc3"><code>4efac9d</code></a> add links</li>
<li><a href="https://github.com/pallets/werkzeug/commit/400c23e01953311bb0959586f7194191732b18bc"><code>400c23e</code></a> Allow flit_core 4.x (<a href="https://redirect.github.com/pallets/werkzeug/issues/3261">#3261</a>)</li>
<li><a href="https://github.com/pallets/werkzeug/commit/7132a19c26320ae01076d2743df42b9913bbe1d7"><code>7132a19</code></a> allow flit_core 4</li>
<li><a href="https://github.com/pallets/werkzeug/commit/6fba87c311e55b4afcef71393a1733498b16676f"><code>6fba87c</code></a> only accept ASCII digits</li>
<li><a href="https://github.com/pallets/werkzeug/commit/263f5caf2e26ebd85e38f899628c22f6813c7a2f"><code>263f5ca</code></a> disallow range -0 (<a href="https://redirect.github.com/pallets/werkzeug/issues/3255">#3255</a>)</li>
<li><a href="https://github.com/pallets/werkzeug/commit/0c419f951f3206c89e7c95155f0bd771b02a961f"><code>0c419f9</code></a> disallow range -0</li>
<li>Additional commits viewable in <a href="https://github.com/pallets/werkzeug/compare/2.2.3...3.1.9">compare view</a></li>
</ul>
</details>
<br />

Updates `jinja2` from 3.1.2 to 3.1.6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/pallets/jinja/releases">jinja2's releases</a>.</em></p>
<blockquote>
<h2>3.1.6</h2>
<p>This is the Jinja 3.1.6 security release, which fixes security issues but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Jinja2/3.1.6/">https://pypi.org/project/Jinja2/3.1.6/</a>
Changes: <a href="https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-6">https://jinja.palletsprojects.com/en/stable/changes/#version-3-1-6</a></p>
<ul>
<li>The <code>|attr</code> filter does not bypass the environment's attribute lookup, allowing the sandbox to apply its checks. <a href="https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7">https://github.com/pallets/jinja/security/advisories/GHSA-cpwx-vrp4-4pq7</a></li>
</ul>
<h2>3.1.5</h2>
<p>This is the Jinja 3.1.5 security fix release, which fixes security issues and bugs but does not otherwise change behavior and should not result in breaking changes compared to the latest feature release.</p>
<p>PyPI: <a href="https://pypi.org/project/Jinja2/3.1.5/">https://pypi.org/project/Jinja2/3.1.5/</a>
Changes: <a href="https://jinja.palletsprojects.com/changes/#version-3-1-5">https://jinja.palletsprojects.com/changes/#version-3-1-5</a>
Milestone: <a href="https://github.com/pallets/jinja/milestone/16?closed=1">https://github.com/pallets/jinja/milestone/16?closed=1</a></p>
<ul>
<li>The sandboxed environment handles indirect calls to <code>str.format</code>, such as by passing a stored reference to a filter that calls its argument. <a href="https://github.com/pallets/jinja/security/advisories/GHSA-q2x7-8rv6-6q7h">GHSA-q2x7-8rv6-6q7h</a></li>
<li>Escape template name before formatting it into error messages, to avoid issues with names that contain f-string syntax. <a href="https://redirect.github.com/pallets/jinja/issues/1792">#1792</a>, <a href="https://github.com/pallets/jinja/security/advisories/GHSA-gmj6-6f8f-6699">GHSA-gmj6-6f8f-6699</a></li>
<li>Sandbox does not allow <code>clear</code> and <code>pop</code> on known mutable sequence types. <a href="https://redirect.github.com/pallets/jinja/issues/2032">#2032</a></li>
<li>Calling sync <code>render</code> for an async template uses <code>asyncio.run</code>. <a href="https://redirect.github.com/pallets/jinja/issues/1952">#1952</a></li>
<li>Avoid unclosed <code>auto_aiter</code> warnings. <a href="https://redirect.github.com/pallets/jinja/issues/1960">#1960</a></li>
<li>Return an <code>aclose</code>-able <code>AsyncGenerator</code> from <code>Template.generate_async</code>. <a href="https://redirect.github.com/pallets/jinja/issues/1960">#1960</a></li>
<li>Avoid leaving <code>root_render_func()</code> unclosed in <code>Template.generate_async</code>. <a href="https://redirect.github.com/pallets/jinja/issues/1960">#1960</a></li>
<li>Avoid leaving async generators unclosed in blocks, includes and extends. <a href="https://redirect.github.com/pallets/jinja/issues/1960">#1960</a></li>
<li>The runtime uses the correct <code>concat</code> function for the current environment when calling block references. <a href="https://redirect.github.com/pallets/jinja/issues/1701">#1701</a></li>
<li>Make <code>|unique</code> async-aware, allowing it to be used after another async-aware filter. <a href="https://redirect.github.com/pallets/jinja/issues/1781">#1781</a></li>
<li><code>|int</code> filter handles <code>OverflowError</code> from scientific notation. <a href="https://redirect.github.com/pallets/jinja/issues/1921">#1921</a></li>
<li>Make compiling deterministic for tuple unpacking in a <code>{% set ... %}</code> call. <a href="https://redirect.github.com/pallets/jinja/issues/2021">#2021</a></li>
<li>Fix dunder protocol (<code>copy</code>/<code>pickle</code>/etc) interaction with <code>Undefined</code> objects. <a href="https://redirect.github.com/pallets/jinja/issues/2025">#2025</a></li>
<li>Fix <code>copy</code>/<code>pickle</code> support for the internal <code>missing</code> object. <a href="https://redirect.github.com/pallets/jinja/issues/2027">#2027</a></li>
<li><code>Environment.overlay(enable_async)</code> is applied correctly. <a href="https://redirect.github.com/pallets/jinja/issues/2061">#2061</a></li>
<li>The error message from <code>FileSystemLoader</code> includes the paths that were searched. <a href="https://redirect.github.com/pallets/jinja/issues/1661">#1661</a></li>
<li><code>PackageLoader</code> shows a clearer error message when the package does not contain the templates directory. <a href="https://redirect.github.com/pallets/jinja/issues/1705">#1705</a></li>
<li>Improve annotations for methods returning copies. <a href="https://redirect.github.com/pallets/jinja/issues/1880">#1880</a></li>
<li><code>urlize</code> does not add <code>mailto:</code> to values like <code>@a@b</code>. <a href="https://redirect.github.com/pallets/jinja/issues/1870">#1870</a></li>
<li>Tests decorated with <code>@pass_context</code> can be used with the <code>|select</code> filter. <a href="https://redirect.github.com/pallets/jinja/issues/1624">#1624</a></li>
<li>Using <code>set</code> for multiple assignment (<code>a, b = 1, 2</code>) does not fail when the target is a namespace attribute. <a href="https://redirect.github.com/pallets/jinja/issues/1413">#1413</a></li>
<li>Using <code>set</code> in all branches of <code>{% if %}{% elif %}{% else %}</code> blocks does not cause the variable to be considered initially undefined. <a href="https://redirect.github.com/pallets/jinja/issues/1253">#1253</a></li>
</ul>
<h2>3.1.4</h2>
<p>This is the Jinja 3.1.4 security release, which fixes security issues and bugs but does not otherwise change behavior and should not result in breaking changes.</p>
<p>PyPI: <a href="https://pypi.org/project/Jinja2/3.1.4/">https://pypi.org/project/Jinja2/3.1.4/</a>
Changes: <a href="https://jinja.palletsprojects.com/en/3.1.x/changes/#version-3-1-4">https://jinja.palletsprojects.com/en/3.1.x/changes/#version-3-1-4</a></p>
<ul>
<li>The <code>xmlattr</code> filter does not allow keys with <code>/</code> solidus, <code>&gt;</code> greater-than sign, or <code>=</code> equals sign, in addition to disallowing spaces. Regardless of any validation done by Jinja, user input should never be used as keys to this filter, or must be separately validated first. GHSA-h75v-3vvj-5mfj</li>
</ul>
<h2>3.1.3</h2>
<p>This is a fix release for the 3.1.x feature branch.</p>
<ul>
<li>Fix for <a href="https://github.com/pallets/jinja/security/advisories/GHSA-h5c8-rqwp-cp95">GHSA-h5c8-rqwp-cp95</a>. You are affected if you are using <code>xmlattr</code> and passing user input as attribute keys.</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pallets/jinja/blob/main/CHANGES.rst">jinja2's changelog</a>.</em></p>
<blockquote>
<h2>Version 3.1.6</h2>
<p>Released 2025-03-05</p>
<ul>
<li>The <code>|attr</code> filter does not bypass the environment's attribute lookup,
allowing the sandbox to apply its checks. :ghsa:<code>cpwx-vrp4-4pq7</code></li>
</ul>
<h2>Version 3.1.5</h2>
<p>Released 2024-12-21</p>
<ul>
<li>The sandboxed environment handles indirect calls to <code>str.format</code>, such as
by passing a stored reference to a filter that calls its argument.
:ghsa:<code>q2x7-8rv6-6q7h</code></li>
<li>Escape template name before formatting it into error messages, to avoid
issues with names that contain f-string syntax.
:issue:<code>1792</code>, :ghsa:<code>gmj6-6f8f-6699</code></li>
<li>Sandbox does not allow <code>clear</code> and <code>pop</code> on known mutable sequence
types. :issue:<code>2032</code></li>
<li>Calling sync <code>render</code> for an async template uses <code>asyncio.run</code>.
:pr:<code>1952</code></li>
<li>Avoid unclosed <code>auto_aiter</code> warnings. :pr:<code>1960</code></li>
<li>Return an <code>aclose</code>-able <code>AsyncGenerator</code> from
<code>Template.generate_async</code>. :pr:<code>1960</code></li>
<li>Avoid leaving <code>root_render_func()</code> unclosed in
<code>Template.generate_async</code>. :pr:<code>1960</code></li>
<li>Avoid leaving async generators unclosed in blocks, includes and extends.
:pr:<code>1960</code></li>
<li>The runtime uses the correct <code>concat</code> function for the current environment
when calling block references. :issue:<code>1701</code></li>
<li>Make <code>|unique</code> async-aware, allowing it to be used after another
async-aware filter. :issue:<code>1781</code></li>
<li><code>|int</code> filter handles <code>OverflowError</code> from scientific notation.
:issue:<code>1921</code></li>
<li>Make compiling deterministic for tuple unpacking in a <code>{% set ... %}</code>
call. :issue:<code>2021</code></li>
<li>Fix dunder protocol (<code>copy</code>/<code>pickle</code>/etc) interaction with <code>Undefined</code>
objects. :issue:<code>2025</code></li>
<li>Fix <code>copy</code>/<code>pickle</code> support for the internal <code>missing</code> object.
:issue:<code>2027</code></li>
<li><code>Environment.overlay(enable_async)</code> is applied correctly. :pr:<code>2061</code></li>
<li>The error message from <code>FileSystemLoader</code> includes the paths that were
searched. :issue:<code>1661</code></li>
<li><code>PackageLoader</code> shows a clearer error message when the package does not
contain the templates directory. :issue:<code>1705</code></li>
<li>Improve annotations for methods returning copies. :pr:<code>1880</code></li>
<li><code>urlize</code> does not add <code>mailto:</code> to values like <code>@a@b</code>. :pr:<code>1870</code></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pallets/jinja/commit/15206881c006c79667fe5154fe80c01c65410679"><code>1520688</code></a> release version 3.1.6</li>
<li><a href="https://github.com/pallets/jinja/commit/90457bbf33b8662926ae65cdde4c4c32e756e403"><code>90457bb</code></a> Merge commit from fork</li>
<li><a href="https://github.com/pallets/jinja/commit/065334d1ee5b7210e1a0a93c37238c86858f2af7"><code>065334d</code></a> attr filter uses env.getattr</li>
<li><a href="https://github.com/pallets/jinja/commit/033c20015c7ca899ab52eb921bb0f08e6d3dd145"><code>033c200</code></a> start version 3.1.6</li>
<li><a href="https://github.com/pallets/jinja/commit/bc68d4efa99c5f77334f0e519628558059ae8c35"><code>bc68d4e</code></a> use global contributing guide (<a href="https://redirect.github.com/pallets/jinja/issues/2070">#2070</a>)</li>
<li><a href="https://github.com/pallets/jinja/commit/247de5e0c5062a792eb378e50e13e692885ee486"><code>247de5e</code></a> use global contributing guide</li>
<li><a href="https://github.com/pallets/jinja/commit/ab8218c7a1b66b62e0ad6b941bd514e3a64a358f"><code>ab8218c</code></a> use project advisory link instead of global</li>
<li><a href="https://github.com/pallets/jinja/commit/b4ffc8ff299dfd360064bea4cd2f862364601ad2"><code>b4ffc8f</code></a> release version 3.1.5 (<a href="https://redirect.github.com/pallets/jinja/issues/2066">#2066</a>)</li>
<li><a href="https://github.com/pallets/jinja/commit/877f6e51be8e1765b06d911cfaa9033775f051d1"><code>877f6e5</code></a> release version 3.1.5</li>
<li><a href="https://github.com/pallets/jinja/commit/8d588592653b052f957b720e1fc93196e06f207f"><code>8d58859</code></a> remove test pypi</li>
<li>Additional commits viewable in <a href="https://github.com/pallets/jinja/compare/3.1.2...3.1.6">compare view</a></li>
</ul>
</details>
<br />

Updates `click` from 8.1.3 to 8.5.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/pallets/click/releases">click's releases</a>.</em></p>
<blockquote>
<h2>8.5.0</h2>
<p>This is the Click 8.5.0 feature release. A feature release may include new features, remove previously deprecated code, add new deprecation, or introduce potentially breaking changes.</p>
<p>We encourage everyone to upgrade. You can read more about our <a href="https://palletsprojects.com/versions">Version Support Policy</a> on our website.</p>
<p>PyPI: <a href="https://pypi.org/project/click/8.5.0/">https://pypi.org/project/click/8.5.0/</a>
Changes:  <a href="https://click.palletsprojects.com/page/changes/#version-8-5-0">https://click.palletsprojects.com/page/changes/#version-8-5-0</a>
Milestone <a href="https://github.com/pallets/click/milestone/33">https://github.com/pallets/click/milestone/33</a></p>
<ul>
<li>Add built-in shell completion support for PowerShell (Windows PowerShell
5.1+ and pwsh 7+) alongside the existing <code>bash</code>, <code>zsh</code>, and <code>fish</code>
completers. Use <code>_FOO_BAR_COMPLETE=powershell_source foo-bar</code> to generate
the completion script. <a href="https://redirect.github.com/pallets/click/issues/2672">#2672</a> <a href="https://redirect.github.com/pallets/click/issues/3637">#3637</a></li>
<li>Supported versions of Windows enable ANSI terminal styles by default.
Colorama is no longer a dependency and is not used. <a href="https://redirect.github.com/pallets/click/issues/2986">#2986</a> <a href="https://redirect.github.com/pallets/click/issues/3505">#3505</a></li>
<li>{class}<code>Argument</code> accepts a <code>help</code> parameter, and help output includes
a <code>Positional arguments</code> section when argument help is available. <a href="https://redirect.github.com/pallets/click/issues/2983">#2983</a> <a href="https://redirect.github.com/pallets/click/issues/3473">#3473</a></li>
<li><code>confirm()</code> and <code>prompt()</code> strip ANSI color and style codes from the
prompt when the output stream does not support them, matching <code>echo()</code>.
This stripping was lost in <code>8.4.0</code> when <a href="https://redirect.github.com/pallets/click/issues/2969">#2969</a> began writing the
prompt with <code>input()</code> directly. <a href="https://redirect.github.com/pallets/click/issues/3572">#3572</a> <a href="https://redirect.github.com/pallets/click/issues/3653">#3653</a></li>
<li>{class}<code>Path</code> with <code>allow_dash=True</code> no longer triggers a <code>BytesWarning</code>,
an error under <code>python -bb</code>, when checking a value against the <code>-</code>
convention. <a href="https://redirect.github.com/pallets/click/issues/2877">#2877</a> <a href="https://redirect.github.com/pallets/click/issues/3642">#3642</a></li>
<li>Add {func}<code>custom_version_option</code>, a <code>--version</code> option whose output is
produced by a callback, covering cases {func}<code>version_option</code> intentionally
does not. The feature set of {func}<code>version_option</code> is now frozen; see
[discussion <a href="https://redirect.github.com/pallets/click/issues/3527">#3527</a>](<a href="https://github.com/pallets/click/discussions/3527">https://github.com/pallets/click/discussions/3527</a>). <a href="https://redirect.github.com/pallets/click/issues/3581">#3581</a></li>
<li><code>style()</code> and <code>secho()</code> no longer silently drop the 256-color index <code>0</code>
(black) passed as <code>fg</code> or <code>bg</code>, and now validate color arguments. Invalid
colors raise a <code>ValueError</code> instead of a <code>TypeError</code>. <a href="https://redirect.github.com/pallets/click/issues/3677">#3677</a></li>
<li>The automatic help option stores its value under the reserved name
<code>_click_default_help</code> instead of <code>help</code>, so a parameter named <code>help</code> no
longer breaks parsing. The new name is visible in
{meth}<code>Command.to_info_dict</code> output. Parameters that overwrite each other's
value trigger a warning: an argument sharing its name with another
parameter, or any parameter claiming the reserved name. Options may still
share a name to compete for the same value (feature switches).
<a href="https://redirect.github.com/pallets/click/issues/2819">#2819</a> <a href="https://redirect.github.com/pallets/click/issues/3678">#3678</a></li>
<li><code>unstyle</code> and the ANSI handling behind help-text wrapping now strip the full
CSI escape-sequence grammar. <a href="https://redirect.github.com/pallets/click/issues/3681">#3681</a></li>
<li>Streamline <code>Option</code> flag handling: the flag-kind, type, lazy-default and
validation steps in <code>Option.__init__</code> move into focused helpers, and
<code>flag_value</code> and <code>default</code> keep their unset sentinel at construction
(resolved lazily on read) so <code>is UNSET</code> reliably tells a user-supplied value
from an auto-derived one. Runtime behavior is unchanged, but
{meth}<code>Parameter.to_info_dict</code> now resolves <code>default=True</code> on a feature
switch to its <code>flag_value</code>, matching what the function receives at call</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pallets/click/blob/main/CHANGES.md">click's changelog</a>.</em></p>
<blockquote>
<h2>Version 8.5.0</h2>
<p>Released 2026-08-24</p>
<ul>
<li>Add built-in shell completion support for PowerShell (Windows PowerShell
5.1+ and pwsh 7+) alongside the existing <code>bash</code>, <code>zsh</code>, and <code>fish</code>
completers. Use <code>_FOO_BAR_COMPLETE=powershell_source foo-bar</code> to generate
the completion script. {issue}<code>2672</code> {pr}<code>3637</code></li>
<li>Supported versions of Windows enable ANSI terminal styles by default.
Colorama is no longer a dependency and is not used. {issue}<code>2986</code> {pr}<code>3505</code></li>
<li>{class}<code>Argument</code> accepts a <code>help</code> parameter, and help output includes
a <code>Positional arguments</code> section when argument help is available. {issue}<code>2983</code> {pr}<code>3473</code></li>
<li><code>confirm()</code> and <code>prompt()</code> strip ANSI color and style codes from the
prompt when the output stream does not support them, matching <code>echo()</code>.
This stripping was lost in <code>8.4.0</code> when {pr}<code>2969</code> began writing the
prompt with <code>input()</code> directly. {issue}<code>3572</code> {pr}<code>3653</code></li>
<li>Fix test failures when using pytest &gt;= 9.1. {pr}<code>3656</code></li>
<li>{class}<code>Path</code> with <code>allow_dash=True</code> no longer triggers a <code>BytesWarning</code>,
an error under <code>python -bb</code>, when checking a value against the <code>-</code>
convention. {issue}<code>2877</code> {pr}<code>3642</code></li>
<li>Add {func}<code>custom_version_option</code>, a <code>--version</code> option whose output is
produced by a callback, covering cases {func}<code>version_option</code> intentionally
does not. The feature set of {func}<code>version_option</code> is now frozen; see
[discussion <a href="https://redirect.github.com/pallets/click/issues/3527">#3527</a>](<a href="https://github.com/pallets/click/discussions/3527">https://github.com/pallets/click/discussions/3527</a>). {pr}<code>3581</code></li>
<li><code>style()</code> and <code>secho()</code> no longer silently drop the 256-color index <code>0</code>
(black) passed as <code>fg</code> or <code>bg</code>, and now validate color arguments. Invalid
colors raise a <code>ValueError</code> instead of a <code>TypeError</code>. {pr}<code>3677</code></li>
<li>The automatic help option stores its value under the reserved name
<code>_click_default_help</code> instead of <code>help</code>, so a parameter named <code>help</code> no
longer breaks parsing. The new name is visible in
{meth}<code>Command.to_info_dict</code> output. Parameters that overwrite each other's
value trigger a warning: an argument sharing its name with another
parameter, or any parameter claiming the reserved name. Options may still
share a name to compete for the same value (feature switches).
{issue}<code>2819</code> {pr}<code>3678</code></li>
<li><code>unstyle</code> and the ANSI handling behind help-text wrapping now strip the full
CSI escape-sequence grammar. {pr}<code>3681</code></li>
<li>Streamline <code>Option</code> flag handling: the flag-kind, type, lazy-default and
validation steps in <code>Option.__init__</code> move into focused helpers, and
<code>flag_value</code> and <code>default</code> keep their unset sentinel at construction
(resolved lazily on read) so <code>is UNSET</code> reliably tells a user-supplied value
from an auto-derived one. Runtime behavior is unchanged, but
{meth}<code>Parameter.to_info_dict</code> now resolves <code>default=True</code> on a feature
switch to its <code>flag_value</code>, matching what the function receives at call
time. {pr}<code>3641</code></li>
<li>{func}<code>get_binary_stream</code> and {func}<code>get_text_stream</code> are deprecated and
will be removed in Click 9.0. {issue}<code>3481</code> {pr}<code>3695</code></li>
<li>The following <code>click.utils</code> names were never intentionally public and are
now private (<code>_</code>-prefixed). The old names remain available with a
<code>DeprecationWarning</code> until Click 9.0: <code>LazyFile</code>, <code>KeepOpenFile</code>,</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pallets/click/commit/8b19813f2bfca99f1018a587a8cf54fc959f2e5d"><code>8b19813</code></a> Release version 8.5.0</li>
<li><a href="https://github.com/pallets/click/commit/2c8cd3ac958a7eb316d67f2d316c27086c4c0369"><code>2c8cd3a</code></a> Add FAQ entry about <code>UnicodeEncodeError</code> on Windows (<a href="https://redirect.github.com/pallets/click/issues/3778">#3778</a>)</li>
<li><a href="https://github.com/pallets/click/commit/131c86aadddfa5cb6dca8339c9d6294c4eacb8ac"><code>131c86a</code></a> Add FAQ entry about <code>UnicodeEncodeError</code> on Windows</li>
<li><a href="https://github.com/pallets/click/commit/e1fd5946ab26aaf372009eaff1acf947140b40fb"><code>e1fd594</code></a> Add support of <code>pathlib.Path</code> to <code>edit</code> (<a href="https://redirect.github.com/pallets/click/issues/3781">#3781</a>)</li>
<li><a href="https://github.com/pallets/click/commit/a1d87858abd77fa8e3ffc204670ccd75b96c4781"><code>a1d8785</code></a> Add support of <code>pathlib.Path</code> to <code>edit</code></li>
<li><a href="https://github.com/pallets/click/commit/2103e157683c5e4cadc8ee1838df526a54bde9a4"><code>2103e15</code></a> Forward all user's parameters set in <code>PAGER</code> and improve flag detection (<a href="https://redirect.github.com/pallets/click/issues/3777">#3777</a>)</li>
<li><a href="https://github.com/pallets/click/commit/a6256bfb5971d5e58585fe7b6c656134e1ade5a4"><code>a6256bf</code></a> Forwards all user's parameters set in <code>PAGER</code></li>
<li><a href="https://github.com/pallets/click/commit/61b69e967e525bd502f5bf42def4d551e761fe0e"><code>61b69e9</code></a> Resolve the pager command once, in <code>_pager_contextmanager</code> (<a href="https://redirect.github.com/pallets/click/issues/3776">#3776</a>)</li>
<li><a href="https://github.com/pallets/click/commit/9835b0f7612d1b1ea180a975fd6d24cf16791ba8"><code>9835b0f</code></a> Resolve the pager command once, in <code>_pager_contextmanager</code></li>
<li><a href="https://github.com/pallets/click/commit/f36d58bbd7f188178de2d4fe1d0292c510375ca7"><code>f36d58b</code></a> Refactor pager stream handling (<a href="https://redirect.github.com/pallets/click/issues/3767">#3767</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/pallets/click/compare/8.1.3...8.5.0">compare view</a></li>
</ul>
</details>
<br />

Updates `requests` from 2.31.0 to 2.34.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/psf/requests/releases">requests's releases</a>.</em></p>
<blockquote>
<h2>v2.34.2</h2>
<h2>2.34.2 (2026-05-14)</h2>
<ul>
<li>Moved <code>headers</code> input type back to <code>Mapping</code> to avoid invariance issues with <code>MutableMapping</code> and inferred dict types. Users calling <code>Request.headers.update()</code> may need to narrow typing in their code. (<a href="https://redirect.github.com/psf/requests/issues/7441">#7441</a>)</li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/psf/requests/blob/main/HISTORY.md#2342-2026-05-14">https://github.com/psf/requests/blob/main/HISTORY.md#2342-2026-05-14</a></p>
<h2>v2.34.1</h2>
<h2>2.34.1 (2026-05-13)</h2>
<p><strong>Bugfixes</strong></p>
<ul>
<li>Widened <code>json</code> input type from <code>dict</code> and <code>list</code> to <code>Mapping</code>
and <code>Sequence</code>. (<a href="https://redirect.github.com/psf/requests/issues/7436">#7436</a>)</li>
<li>Changed <code>headers</code> input type to MutableMapping and removed <code>None</code> from
<code>Request.headers</code> typing to improve handling for users. (<a href="https://redirect.github.com/psf/requests/issues/7431">#7431</a>)</li>
<li><code>Response.reason</code> moved from <code>str | None</code> to <code>str</code> to improve handling
for users. (<a href="https://redirect.github.com/psf/requests/issues/7437">#7437</a>)</li>
<li>Fixed a bug where some bodies with custom <code>__getattr__</code> implementations
weren't being properly detected as Iterables. (<a href="https://redirect.github.com/psf/requests/issues/7433">#7433</a>)</li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/k223kim"><code>@​k223kim</code></a> made their first contribution in <a href="https://redirect.github.com/psf/requests/pull/7433">psf/requests#7433</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/psf/requests/blob/main/HISTORY.md#2341-2026-05-13">https://github.com/psf/requests/blob/main/HISTORY.md#2341-2026-05-13</a></p>
<h2>v2.34.0</h2>
<h2>2.34.0 (2026-05-11)</h2>
<p><strong>Announcements</strong></p>
<ul>
<li>
<p>Requests 2.34.0 introduces inline types, replacing those provided by
typeshed. Public API types should be fully compatible with mypy, pyright,
and ty. <strong>We believe types are comprehensive but if you find issues, please
report them to the <a href="https://redirect.github.com/psf/requests/issues/7271">pinned tracking issue</a>.</strong></p>
<p>Special thanks to <a href="https://github.com/bastimeyer"><code>@​bastimeyer</code></a>, <a href="https://github.com/cthoyt"><code>@​cthoyt</code></a>, <a href="https://github.com/edgarrmondragon"><code>@​edgarrmondragon</code></a>, and <a href="https://github.com/srittau"><code>@​srittau</code></a> for
helping review and test the types ahead of the release. (<a href="https://redirect.github.com/psf/requests/issues/7272">#7272</a>)</p>
</li>
</ul>
<p><strong>Improvements</strong></p>
<ul>
<li>Digest Auth hashing algorithms have added <code>usedforsecurity=False</code> to clarify
security considerations. (<a href="https://redirect.github.com/psf/requests/issues/7310">#7310</a>)</li>
<li>Requests added support for Python 3.15 based on beta1. Downstream projects
should be able to start testing prior to its release in October. (<a href="https://redirect.github.com/psf/requests/issues/7422">#7422</a>)</li>
<li>Requests added support for Python 3.14t. (<a href="https://redirect.github.com/psf/requests/issues/7419">#7419</a>)</li>
</ul>
<p><strong>Bugfixes</strong></p>
<ul>
<li><code>Response.history</code> no longer contains a reference to itself, preventing
accidental looping when traversing the history list. (<a href="https://redirect.github.com/psf/requests/issues/7328">#7328</a>)</li>
<li>Requests no longer performs greedy matching on no_proxy domains. The</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/psf/requests/blob/main/HISTORY.md">requests's changelog</a>.</em></p>
<blockquote>
<h2>2.34.2 (2026-05-14)</h2>
<ul>
<li>Moved <code>headers</code> input type back to <code>Mapping</code> to avoid invariance issues
with <code>MutableMapping</code> and inferred dict types. Users calling
<code>Request.headers.update()</code> may need to narrow typing in their code. (<a href="https://redirect.github.com/psf/requests/issues/7441">#7441</a>)</li>
</ul>
<h2>2.34.1 (2026-05-13)</h2>
<p><strong>Bugfixes</strong></p>
<ul>
<li>Widened <code>json</code> input type from <code>dict</code> and <code>list</code> to <code>Mapping</code>
and <code>Sequence</code>. (<a href="https://redirect.github.com/psf/requests/issues/7436">#7436</a>)</li>
<li>Changed <code>headers</code> input type to MutableMapping and removed <code>None</code> from
<code>Request.headers</code> typing to improve handling for users. (<a href="https://redirect.github.com/psf/requests/issues/7431">#7431</a>)</li>
<li><code>Response.reason</code> moved from <code>str | None</code> to <code>str</code> to improve handling
for users. (<a href="https://redirect.github.com/psf/requests/issues/7437">#7437</a>)</li>
<li>Fixed a bug where some bodies with custom <code>__getattr__</code> implementations
weren't being properly detected as Iterables. (<a href="https://redirect.github.com/psf/requests/issues/7433">#7433</a>)</li>
</ul>
<h2>2.34.0 (2026-05-11)</h2>
<p><strong>Announcements</strong></p>
<ul>
<li>
<p>Requests 2.34.0 introduces inline types, replacing those provided by
typeshed. Public API types should be fully compatible with mypy, pyright,
and ty. We believe types are comprehensive but if you find issues, please
report them to the pinned tracking issue.</p>
<p>Special thanks to <a href="https://github.com/bastimeyer"><code>@​bastimeyer</code></a>, <a href="https://github.com/cthoyt"><code>@​cthoyt</code></a>, <a href="https://github.com/edgarrmondragon"><code>@​edgarrmondragon</code></a>, and <a href="https://github.com/srittau"><code>@​srittau</code></a> for
helping review and test the types ahead of the release. (<a href="https://redirect.github.com/psf/requests/issues/7272">#7272</a>)</p>
</li>
</ul>
<p><strong>Improvements</strong></p>
<ul>
<li>Digest Auth hashing algorithms have added <code>usedforsecurity=False</code> to clarify
security considerations. (<a href="https://redirect.github.com/psf/requests/issues/7310">#7310</a>)</li>
<li>Requests added support for Python 3.15 based on beta1. Downstream projects
should be able to start testing prior to its release in October. (<a href="https://redirect.github.com/psf/requests/issues/7422">#7422</a>)</li>
<li>Requests added support for Python 3.14t. (<a href="https://redirect.github.com/psf/requests/issues/7419">#7419</a>)</li>
</ul>
<p><strong>Bugfixes</strong></p>
<ul>
<li><code>Response.history</code> no longer contains a reference to itself, preventing
accidental looping when traversing the history list. (<a href="https://redirect.github.com/psf/requests/issues/7328">#7328</a>)</li>
<li>Requests no longer performs greedy matching on no_proxy domains. The
proxy_bypass implementation has been updated with CPython's fix from
bpo-39057. (<a href="https://redirect.github.com/psf/requests/issues/7427">#7427</a>)</li>
<li>Requests no longer incorrectly strips duplicate leading slashes in
URI paths. This should address user issues with specific presigned
URLs. Note the full fix requires urllib3 2.7.0+. (<a href="https://redirect.github.com/psf/requests/issues/7315">#7315</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/psf/requests/commit/6e83187b8feb273ed4c6cdab5efd8d54901dfab3"><code>6e83187</code></a> v2.34.2</li>
<li><a href="https://github.com/psf/requests/commit/84d10f0be83e8f6aeca8a05230c52216431c4d0b"><code>84d10f0</code></a> Move Request.headers back to Mapping (<a href="https://redirect.github.com/psf/requests/issues/7441">#7441</a>)</li>
<li><a href="https://github.com/psf/requests/commit/b7b549b54571d03950b16afd2d01bc6ff0348224"><code>b7b549b</code></a> v2.34.1</li>
<li><a href="https://github.com/psf/requests/commit/e511bc72777a94c45d004e010c597925092e1efe"><code>e511bc7</code></a> Fix mutability issues with headers input types (<a href="https://redirect.github.com/psf/requests/issues/7431">#7431</a>)</li>
<li><a href="https://github.com/psf/requests/commit/5691f596134c2feb121e595c77a0178921fcce61"><code>5691f59</code></a> Update JsonType containers to read-based collections (<a href="https://redirect.github.com/psf/requests/issues/7436">#7436</a>)</li>
<li><a href="https://github.com/psf/requests/commit/2144213c307691710c9d665700860fc4993c3035"><code>2144213</code></a> Constrain Response.reason to str (<a href="https://redirect.github.com/psf/requests/issues/7437">#7437</a>)</li>
<li><a href="https://github.com/psf/requests/commit/6404f345e562d962abe6700a1c357ec1e7e18232"><code>6404f34</code></a> Fix <code>prepare_body</code> stream detection for <code>__getattr__</code>-based file wrappers (<a href="https://redirect.github.com/psf/requests/issues/7">#7</a>...</li>
<li><a href="https://github.com/psf/requests/commit/0b401c76b6e80a4eecf3c690085b2553f6e261ca"><code>0b401c7</code></a> v2.34.0</li>
<li><a href="https://github.com/psf/requests/commit/86b378d3f60f828daa13ca50aa82e287ff7b66b4"><code>86b378d</code></a> Align Session.get parameters with requests.get (<a href="https://redirect.github.com/psf/requests/issues/7429">#7429</a>)</li>
<li><a href="https://github.com/psf/requests/commit/a4f9a5999bdb9bf2d6e7c8aa973b28cacb17134f"><code>a4f9a59</code></a> Port bpo-39057 to Requests (<a href="https://redirect.github.com/psf/requests/issues/7427">#7427</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/psf/requests/compare/v2.31.0...v2.34.2">compare view</a></li>
</ul>
</details>
<br />

Updates `urllib3` from 1.26.18 to 2.8.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/urllib3/urllib3/releases">urllib3's releases</a>.</em></p>
<blockquote>
<h2>2.8.0</h2>
<h2>🚀 urllib3 is fundraising for HTTP/2 support</h2>
<p><a href="https://sethmlarson.dev/urllib3-is-fundraising-for-http2-support">urllib3 is raising ~$40,000 USD</a> to release HTTP/2 support and ensure long-term sustainable maintenance of the project. If your company or organization uses Python and would benefit from HTTP/2 support in Requests, pip, cloud SDKs, and thousands of other projects <a href="https://opencollective.com/urllib3">please consider contributing financially</a> to ensure HTTP/2 support is developed sustainably and maintained for the long-haul.</p>
<p>Thank you for your support.</p>
<h2>Security</h2>
<p>Fixed the following security issues:</p>
<ul>
<li>The TLS configuration for HTTPS proxies could be ignored or overridden. (High severity, GHSA-8988-9cw3-xx77)</li>
<li><code>HTTPResponse.stream()</code> and <code>read_chunked()</code> could buffer a chunk-size line of unbounded length in memory. (High severity, GHSA-vxq7-64xx-v4gw)</li>
<li>Chunked Deflate streaming could enter an infinite loop. (Medium severity, GHSA-gh4c-6fx4-qh6g)</li>
</ul>
<blockquote>
<p>[!IMPORTANT]
urllib3 2.8.0 fixes HTTPS proxy TLS configuration being ignored or overridden by destination settings. Configurations relying on that behavior may require changes.</p>
<p>Configure proxy CA certificates and client certificates in <code>proxy_ssl_context</code>, and proxy identity checks with <code>proxy_assert_hostname</code> or <code>proxy_assert_fingerprint</code>. Destination client certificates and identity overrides no longer apply to HTTPS forwarding proxy connections.</p>
</blockquote>
<blockquote>
<p>[!NOTE]
CVE IDs had not yet been assigned to these advisories at the time of release due to a backlog at GitHub's CNA.</p>
</blockquote>
<h2>Deprecations &amp; Removals</h2>
<ul>
<li>Deprecated using an empty collection as the <code>Retry</code> option <code>allowed_methods</code> to retry any verb. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5044">#5044</a>)</li>
</ul>
<h2>Features</h2>
<ul>
<li>Added <code>Url.auth_decoded</code> and <code>Url.auth_decoded_joined</code> convenience properties to the result of <code>parse_url()</code>. (<a href="https://redirect.github.com/urllib3/urllib3/issues/4945">#4945</a>)</li>
<li>Added <code>basic_auth_encoding</code> and <code>proxy_basic_auth_encoding</code> parameters to <code>urllib3.util.make_headers()</code>. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5092">#5092</a>)</li>
</ul>
<h2>Bugfixes</h2>
<ul>
<li>
<p>Fixed response header handling to replace obsolete folded header lines (<code>obs-fold</code>) with spaces in accordance with RFC 9112, preventing raw CRLF sequences from appearing in header values such as <code>Set-Cookie</code>. (<a href="https://redirect.github.com/urllib3/urllib3/issues/1362">#1362</a>)</p>
</li>
<li>
<p>Fixed usage of <code>proxy_ssl_context</code> with <code>ProxyManager</code> when <code>use_forwarding_for_https=True</code>. Passing <code>ssl_context</code> instead of <code>proxy_ssl_context</code> for HTTPS proxies in this configuration now emits a <code>FutureWarning</code> and will raise an error in v3.0. (<a href="https://redirect.github.com/urllib3/urllib3/issues/2577">#2577</a>)</p>
</li>
<li>
<p>Changed behavior of the default <code>ConnectionPool.pool</code> initialization. <code>LifoQueue</code> is now resolved from the <code>queue</code> module after the <code>ConnectionPool</code> is instantiated instead of using the default cached <code>QueueCls</code> class property. This is done because sometimes the <code>queue.LifoQueue</code> is monkey-patched late in the program, such as by gevent. (<a href="https://redirect.github.com/urllib3/urllib3/issues/3289">#3289</a>)</p>
</li>
<li>
<p>Raised <code>UnrewindableBodyError</code> instead of <code>ValueError</code> when retrying a request whose body had <code>tell()</code> but not <code>seek()</code>. (<a href="https://redirect.github.com/urllib3/urllib3/issues/3779">#3779</a>)</p>
</li>
<li>
<p>Decoded percent-encoded SOCKS proxy credentials before authenticating with the proxy server. (<a href="https://redirect.github.com/urllib3/urllib3/issues/3785">#3785</a>)</p>
</li>
<li>
<p>Fixed <code>HTTPResponse.drain_conn()</code> to discard unread response data in 64 KiB chunks (same as the default <code>amt</code> when doing <code>HTTPResponse.stream(...)</code>). (<a href="https://redirect.github.com/urllib3/urllib3/issues/5019">#5019</a>)</p>
</li>
<li>
<p>Fixed <code>is_ipaddress()</code> to detect non-standard IPv4 forms accepted by <code>socket.connect</code>, such as hex (<code>0x7f000001</code>), octal (<code>0177.0.0.1</code>), and decimal integers (<code>2130706433</code>), ensuring SSL certificate verification uses the correct mode for these addresses. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5029">#5029</a>)</p>
</li>
<li>
<p>Fixed <code>HTTPConnectionPool.urlopen</code> raising a misleading <code>FullPoolError</code> instead of <code>ValueError</code> when called with an invalid <code>timeout</code> argument on a pool created with <code>block=True</code>. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5059">#5059</a>)</p>
</li>
<li>
<p>Fixed port-zero handling to preserve explicit <code>:0</code> values instead of substituting the default ports 80 or 443 in URL parsing, pool selection, proxy configuration, <code>connection_from_url()</code>, and HTTP/2 request authority. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5071">#5071</a>, <a href="https://redirect.github.com/urllib3/urllib3/issues/5101">#5101</a>)</p>
</li>
<li>
<p>Fixed a bug where <code>PoolManager</code> passed the <code>assert_hostname</code> and <code>assert_fingerprint</code> parameters to HTTP connection pools. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5077">#5077</a>)</p>
</li>
<li>
<p>Fixed <code>HTTPConnectionPool.urlopen()</code> and HTTP proxy forwarding to strip URL fragments from absolute request targets before sending requests. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5079">#5079</a>)</p>
</li>
<li>
<p>Added safeguards to the proxy tunneling code to prevent potential security issues when handling invalid characters in the proxy host and HTTP headers. This change affects users of Python 3.10, Python 3.11, and Python 3.12 when the standard library does not contain the fix; those on newer Python versions should upgrade to 3.13.14+ or 3.14.5+ to get the same security fixes. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5091">#5091</a>)</p>
</li>
<li>
<p>Fixed <code>HTTPSConnection.connect()</code> overriding <code>ProxyConfig.ssl_context</code>'s certificate policy and proxy identity checks with the target connection's TLS settings when forwarding through an HTTPS proxy.</p>
<p><code>HTTPSConnection</code> no longer applies target SNI, assertions, or client credentials to forwarding proxy handshakes and continues to use its <code>ssl_context</code> as a fallback when an HTTPS proxy forwards an HTTP target. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5093">#5093</a>)</p>
</li>
<li>
<p>Fixed URL parsing to more strictly enforce RFC 3986 host syntax, rejecting invalid host input such as raw spaces and control characters, malformed percent-encodings, and percent-encoded control characters in HTTP(S) hosts and IPv6 zone identifiers, including proxy CONNECT tunnel targets. Host normalization now also follows RFC 3986 normalization rules for percent-encoded octets by decoding percent-encoded unreserved characters and uppercasing the hexadecimal digits of retained percent-encoded octets. (<a href="https://redirect.github.com/urllib3/urllib3/issues/5095">#5095</a>)</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/urllib3/urllib3/blob/main/CHANGES.rst">urllib3's changelog</a>.</em></p>
<blockquote>
<h1>2.8.0 (2026-09-15)</h1>
<h2>Security</h2>
<p>Fixed the following security issues:</p>
<ul>
<li>The TLS configuration for HTTPS proxies could be ignored or overridden.
(High severity, <code>GHSA-8988-9cw3-xx77 &lt;https://github.com/urllib3/urllib3/security/advisories/GHSA-8988-9cw3-xx77&gt;...

_Description has been truncated_