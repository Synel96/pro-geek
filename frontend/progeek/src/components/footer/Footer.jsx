import React from "react";
import Box from "@mui/joy/Box";
import Typography from "@mui/joy/Typography";

export default function Footer() {
  return (
    <Box
      component="footer"
      role="contentinfo"
      aria-label="Oldal lábléc"
      sx={{
        width: "100%",
        py: 2,
        bgcolor: "background.level1",
        color: "text.secondary",
        textAlign: "center",
        fontFamily: "var(--joy-fontFamily-body, inherit)",
        fontSize: { xs: 13, sm: 15 },
        mt: 6,
        position: "relative",
        "&::before": {
          content: '""',
          display: "block",
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: 3,
          background: "linear-gradient(90deg, #783cdc 0%, #b47aff 100%)",
          boxShadow: "0 0 6px 1px #783cdc, 0 0 16px 2px #b47aff",
          borderRadius: 8,
          opacity: 0.85,
          zIndex: 1,
        },
      }}
    >
      <Typography level="body2" aria-label="Jogi nyilatkozat">
        Minden jog fenntartva. &copy; ProGeek 2025
      </Typography>
    </Box>
  );
}
