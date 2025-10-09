import React from "react";
import { useColorScheme } from "@mui/joy/styles";
import pikachuSrcSet from "../../../assets/pikachu.png?w=32;webp;avif&as=srcset";
import pikachuPng from "../../../assets/pikachu.png?w=32&as=src";
import gastlySrcSet from "../../../assets/gastly.png?w=32;webp;avif&as=srcset";
import gastlyPng from "../../../assets/gastly.png?w=32&as=src";
import Box from "@mui/joy/Box";
import IconButton from "@mui/joy/IconButton";
import Tooltip from "@mui/joy/Tooltip";

// Pikachu és Gastly ikon - csak sima emelkedés hoverre, glow nélkül
function IconImg({ srcSet, fallback, alt }) {
  const [hover, setHover] = React.useState(false);
  const transform = hover ? "translateY(-6px) scale(1.08)" : "none";

  return (
    <picture>
      <source srcSet={srcSet} type="image/avif, image/webp" />
      <img
        src={fallback}
        alt={alt}
        width={32}
        height={32}
        loading="eager"
        fetchPriority="high"
        style={{
          opacity: 1,
          transition: "opacity 0.18s, transform 0.18s cubic-bezier(.4,2,.6,1)",
          cursor: "pointer",
          display: "block",
          transform,
        }}
        draggable={false}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        onFocus={() => setHover(true)}
        onBlur={() => setHover(false)}
      />
    </picture>
  );
}

export default function ColorModeSwitcher() {
  const { mode, setMode } = useColorScheme();

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      {mode === "dark" ? (
        <Tooltip title="Világos mód (Pikachu)">
          <IconButton
            aria-label="Világos mód"
            onClick={() => setMode("light")}
            variant="plain"
            color="neutral"
            sx={{
              boxShadow: "none !important",
              background: "none !important",
              p: 0,
              m: 0,
              minWidth: 0,
              minHeight: 0,
              border: "none",
              "&:hover": { background: "none", boxShadow: "none" },
            }}
          >
            <IconImg
              srcSet={pikachuSrcSet}
              fallback={pikachuPng}
              alt="Pikachu"
            />
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Sötét mód (Gastly)">
          <IconButton
            aria-label="Sötét mód"
            onClick={() => setMode("dark")}
            variant="plain"
            color="neutral"
            sx={{
              boxShadow: "none !important",
              background: "none !important",
              p: 0,
              m: 0,
              minWidth: 0,
              minHeight: 0,
              border: "none",
              "&:hover": { background: "none", boxShadow: "none" },
            }}
          >
            <IconImg srcSet={gastlySrcSet} fallback={gastlyPng} alt="Gastly" />
          </IconButton>
        </Tooltip>
      )}
    </Box>
  );
}
