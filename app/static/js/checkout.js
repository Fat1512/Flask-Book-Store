document.querySelectorAll('input[name="address"]').forEach((radio) => {
    radio.addEventListener('change', (e) => {
        const prev = document.querySelector(".active")
        prev.classList.remove("active")
        const activeAddress = document.getElementById(e.target.value)
        activeAddress.classList.add("active")
    });
});