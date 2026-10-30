/**
 * Keep the site on extensionless URLs.
 *
 * Cloudflare's "drop-trailing-slash" HTML handling serves /blog from
 * blog.html. This Worker adds permanent redirects from the old /blog.html
 * and /blog/ URLs so only one URL is ever indexed.
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === "/index" || path === "/index.html") {
      return Response.redirect(new URL("/", url).toString(), 301);
    }

    if (path.endsWith(".html")) {
      return Response.redirect(new URL(path.slice(0, -5) + url.search, url).toString(), 301);
    }

    if (path.length > 1 && path.endsWith("/")) {
      const target = path.replace(/\/+$/, "");
      const destination = target === "/index" ? "/" : target;
      return Response.redirect(new URL(destination + url.search, url).toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};
