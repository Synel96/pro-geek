import React from "react";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";
import useMediaQuery from "@mui/material/useMediaQuery";
import OptimizedImage from "../OptimizedImage";
import { Link } from "react-router-dom";
import { LOGO_GLOW, LOGO_EMBOSS, LOGO_SIZE } from "./logoConfig";
import { logoSrcSet, logoPng } from "./logoAssets";

export default function Logo({ hideText = false }) {
  const isMobile = useMediaQuery("(max-width:600px)");
  const size = LOGO_SIZE(isMobile);

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: isMobile ? "center" : "flex-start",
        height: "100%",
        width: "auto",
        gap: 2,
        p: 0,
        flex: isMobile ? 1 : undefined,
      }}
    >
      <Link
        to="/"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "2px 4px", // 🔹 minimal padding
        }}
        tabIndex={0}
        aria-label="Főoldal"
        onMouseEnter={(e) =>
          e.currentTarget
            .querySelector(".progeek-logo-img")
            .classList.add("glow-on")
        }
        onMouseLeave={(e) =>
          e.currentTarget
            .querySelector(".progeek-logo-img")
            .classList.remove("glow-on")
        }
        onFocus={(e) =>
          e.currentTarget
            .querySelector(".progeek-logo-img")
            .classList.add("glow-on")
        }
        onBlur={(e) =>
          e.currentTarget
            .querySelector(".progeek-logo-img")
            .classList.remove("glow-on")
        }
      >
        <OptimizedImage
          srcSet={logoSrcSet}
          fallback={logoPng}
          alt="ProGeek logó"
          width={size}
          height={size}
          className="progeek-logo-img"
          fetchPriority="high"
          sizes="(max-width: 600px) 100px, 140px"
        />
      </Link>

      {!hideText && (
        <Typography
          level="h2"
          sx={{
            fontWeight: 800,
            letterSpacing: 1,
            display: { xs: "none", sm: "block" },
            color: "text.primary",
            textShadow: LOGO_EMBOSS,
            filter: LOGO_GLOW,
            WebkitFilter: LOGO_GLOW,
            lineHeight: 1,
          }}
        >
          ProGeek
        </Typography>
      )}
    </Box>
  );
}
