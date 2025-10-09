import React from "react";
import Box from "@mui/joy/Box";
import IconButton from "@mui/joy/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import useMediaQuery from "@mui/material/useMediaQuery";
import { Link } from "react-router-dom";
import Logo from "./Logo";
import MobileDrawerMenu from "./MobileDrawerMenu";
import MenuButton from "./MenuButton";
import ColorModeSwitcher from "./ColorModeSwitcher";

export default function Navbar() {
  const isMobile = useMediaQuery("(max-width:600px)");
  const [open, setOpen] = React.useState(false);

  const navLinks = [
    { to: "/", label: "Főoldal" },
    { to: "/news", label: "Hírek" },
    { to: "/about", label: "Rólunk" },
    { to: "/bejelentkezes", label: "Bejelentkezés" },
  ];

  return (
    <Box
      component="nav"
      sx={{
        width: "100%",
        px: 0.5,
        py: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        bgcolor: "background.body",
        color: "text.primary",
        minHeight: 36,
        boxShadow: 2,
        pr: { xs: 1, sm: 1.5, md: 2 },
        position: "relative",
        borderBottom: "none",
        "&::after": {
          content: '""',
          display: "block",
          position: "absolute",
          bottom: 0,
          left: 0,
          width: "100%",
          height: 3,
          background: "linear-gradient(90deg, #50C3D0 0%, #00ffd0 100%)",
          boxShadow: "0 0 6px 1px #50C3D0, 0 0 16px 2px #00ffd0",
          borderRadius: 8,
          opacity: 0.85,
          zIndex: 2,
        },
      }}
      aria-label="Fő navigáció"
    >
      <Logo hideText aria-label="ProGeek főoldal logó" tabIndex={0} />

      {isMobile ? (
        <>
          <IconButton
            aria-label="Menü megnyitása"
            onClick={() => setOpen(true)}
            variant="plain"
            sx={{
              ml: "auto",
              mr: { xs: 1.2, sm: 1.5 },
              minWidth: 40,
              minHeight: 40,
              borderRadius: 2,
              transition: "background 0.18s, box-shadow 0.18s",
              "&:focus-visible": {
                outline: "2px solid #50C3D0",
                boxShadow: "0 0 0 4px rgba(80,195,208,0.15)",
              },
            }}
          >
            <MenuIcon />
          </IconButton>

          <MobileDrawerMenu
            open={open}
            onClose={() => setOpen(false)}
            navLinks={navLinks}
          />
        </>
      ) : (
        <Box
          sx={{
            display: "flex",
            gap: 2,
            pr: { xs: 1.5, sm: 2, md: 4 },
            alignItems: "center",
            ml: "auto",
          }}
        >
          {navLinks.map((link) => (
            <MenuButton
              key={link.to}
              component={Link}
              to={link.to}
              aria-label={link.label}
            >
              {link.label}
            </MenuButton>
          ))}
          <ColorModeSwitcher />
        </Box>
      )}
    </Box>
  );
}
