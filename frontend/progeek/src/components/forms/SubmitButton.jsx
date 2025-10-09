import React from "react";
import Button from "@mui/joy/Button";

export default function SubmitButton({ children, sx = {}, ...props }) {
  return (
    <Button
      type="submit"
      variant="solid"
      color="primary"
      sx={{
        mt: 2,
        fontWeight: 600,
        fontFamily: "var(--joy-fontFamily-body, inherit)",
        ...sx,
      }}
      fullWidth
      {...props}
    >
      {children}
    </Button>
  );
}
