import React from "react";

/**
 * Universal, accessible, responsive image component for vite-imagetools srcset (webp/avif fallback).
 * Usage: <OptimizedImage srcSet={logoSrcSet} fallback={logoPng} alt="..." width={...} height={...} sizes="..." fetchPriority="high" />
 */
export default function OptimizedImage({
  srcSet,
  fallback,
  alt = "",
  width,
  height,
  sizes = "100vw",
  style = {},
  className = "",
  fetchPriority = undefined,
  ...props
}) {
  return (
    <picture>
      <source srcSet={srcSet} type="image/avif, image/webp" sizes={sizes} />
      <img
        src={fallback}
        alt={alt}
        width={width}
        height={height}
        sizes={sizes}
        loading={fetchPriority === "high" ? undefined : "lazy"}
        fetchPriority={fetchPriority}
        style={{ maxWidth: "100%", height: "auto", ...style }}
        className={className}
        {...props}
      />
    </picture>
  );
}
