// Update copyright year dynamically
document.addEventListener('DOMContentLoaded', function() {
    const copyrightElement = document.getElementById('copyright');
    if (copyrightElement) {
        const currentYear = new Date().getFullYear();
        const copyrightText = copyrightElement.innerHTML;
        const updatedText = copyrightText.replace(/\d{4} - \d{4}/, `2024 - ${currentYear}`);
        copyrightElement.innerHTML = updatedText;
    }
});
