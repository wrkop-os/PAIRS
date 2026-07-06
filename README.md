# Dynamic GC — Cinematic Landing Page

Single-file website for Dynamic GC Corp, a general contractor serving the five boroughs of
New York City (roofing, waterproofing, masonry, renovations, restoration and facility services).

## Structure

```
index.html   # the entire site — HTML, CSS, and JS in one self-contained file
```

The page is a scroll-driven WebGL experience (Three.js r160 via unpkg importmap): a bronze
sculpture centerpiece with a full 360° camera orbit tied to scroll, forge-spark particles,
a liquid-metal background shader that shifts bronze→sapphire as you scroll, parallax editorial
slides with per-letter blur-up reveals, animated stat counters, a custom two-ring cursor, and
a stories-style progress bar.

No build step — serve the file with any static host (Vercel, Netlify, GitHub Pages).
Three.js, fonts, and the 3D/image assets load from CDNs at runtime, so an internet
connection is required.

## Company facts

Address, phone, service lines, and history are from Dynamic GC Corp's public listings
(dynamicgcc.com, BBB, The Blue Book). Edit `index.html` to update copy.
