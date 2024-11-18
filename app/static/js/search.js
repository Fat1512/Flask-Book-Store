const sub_item = document.querySelectorAll(".sub-item")
sub_item.forEach(s => {
    async function handleOnClick(id) {
        const res = await fetch(`/api/v1/bookGerne?gerneId=${id}`)
        if (!res.ok) throw Error("Failed getting book gerne")
        const data = await res.json()
        render_gerne(data.current_gerne, data.sub_gerne)
    }

    s.addEventListener("click", () => handleOnClick(s.id))
})
const render_gerne =function (current_gerne, sub_gerne) {
    render_parent_gerne()
    render_current_gerne(current_gerne)
    render_sub_gerne(sub_gerne)
}

const render_parent_gerne = function () {
    const parent = document.querySelector(".parent-gerne")
    const current = document.querySelector(".selected-filter")
    parent.insertAdjacentHTML("afterbegin", `<li><span>${current.textContent}</span></li>`)

}

const render_current_gerne = function (book_gerne) {
    const el = document.querySelector(".current-gerne")
    console.log(book_gerne)
    el.innerHTML = `
         <span class="selected-filter">${book_gerne[0].name}</span>
    `
}
const render_sub_gerne = function (books_gerne) {
    const el = document.querySelector(".children-gerne")
    const html = books_gerne.map(b => `
         <li><span class="sub-item" id="${b.id}">${b.name}</span></li>
    `).join("")

    el.innerHTML = html
}