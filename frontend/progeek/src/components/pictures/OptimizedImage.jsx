import React from "react";

/**
 * Universal, accessible, responsive image component for Cloudinary images (f_auto param már backendből jön).
 * Usage: <OptimizedImage src={cloudinaryUrl} alt="..." width={...} height={...} sizes="..." />
 */
export default function OptimizedImage({
  src,
  alt = "",
  width,
  height,
  sizes = "100vw",
  style = {},
  className = "",
  ...props
}) {
  // Accessibility: alt is required, width/height for layout shift prevention
  // Responsive: sizes prop, style: maxWidth: "100%", height: "auto"
  return (
    <img
      src={src}
      alt={alt}
      width={width}
      height={height}
      sizes={sizes}
      loading="lazy"
      style={{ maxWidth: "100%", height: "auto", ...style }}
      className={className}
      {...props}
    />
  );
}
