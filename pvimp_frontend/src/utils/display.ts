export function displayUnitName(
  value: string | null | undefined
): string {
  if (!value) {
    return "-";
  }

  return value
    .replace(/^\s*2\s*-\s*/u, "")
    .replace(/^\s*2\s+(?=[\u0600-\u06FF])/u, "")
    .replace(/^\s*2(?=[\u0600-\u06FF])/u, "")
    .trim();
}
