function copyToClipboard(id) {
  const input = document.getElementById(id);
  if (!input) {
    alert("Error: Element not found.");
    return;
  }
  navigator.clipboard.writeText(input.value).then(() => {
    alert("Password copied to clipboard.");
  }).catch(err => {
    alert("Failed to copy password: " + err);
  });
}
