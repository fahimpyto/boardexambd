/**
 * Serve the site's .html URLs unchanged and keep "/" as the homepage.
 *
 * Cloudflare's default HTML handling redirects /page.html to /page. The site's
 * canonical URLs use .html, so HTML handling is disabled in wrangler.jsonc.
 * This Worker only restores the root route and redirects /index.html to /.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/index.html") {
      return Response.redirect(new URL("/", url).toString(), 301);
    }

    if (url.pathname === "/") {
      const index = new URL("/index.html", url);
      return env.ASSETS.fetch(new Request(index, request));
    }

    return env.ASSETS.fetch(request);
  },
};
