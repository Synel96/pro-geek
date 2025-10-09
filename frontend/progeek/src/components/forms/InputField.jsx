import Input from "@mui/joy/Input";

export default function InputField({
  value,
  onChange,
  placeholder,
  type = "text",
  name,
  autoComplete,
  sx = {},
  ...props
}) {
  return (
    <Input
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      type={type}
      name={name}
      autoComplete={autoComplete}
      variant="plain"
      slotProps={{
        input: {
          style: {
            outline: "none",
          },
        },
      }}
      sx={{
        bgcolor: "background.body",
        border: "1px solid",
        borderColor: "primary.300",
        borderRadius: "md",
        color: "text.primary",
        fontFamily: "var(--joy-fontFamily-body, inherit)",
        transition: "border-color 0.18s, box-shadow 0.18s",
        boxShadow: "none",
        outline: "none",

        "&:focus-within": {
          borderColor: "secondary.500",
          boxShadow: "0 0 0 2px rgba(120,60,220,0.25)",
          outline: "none",
        },

        "& input": {
          outline: "none !important", // ez tiltja le a böngésző keretet is
          boxShadow: "none !important",
        },

        ...sx,
      }}
      {...props}
    />
  );
}
