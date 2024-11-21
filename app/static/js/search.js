//API
const BOOK_GERNE_API = '/api/v1/bookGerne'
const currentUrl = new URL(window.location);
// DECLARE VARIABLE
var margin = 0

//DECALE FUNCTION
async function fetchGerne(id) {
    const res = await fetch(`${BOOK_GERNE_API}?gerneId=${id}`)
    if (!res.ok) throw Error("Failed getting book gerne")
    const data = await res.json()
    return data
}

function showSpinner() {
    document.querySelector('.spinner').style.display = 'block';
    document.querySelector('.overlay').style.display = 'block';
    console.log("ok")
}

// Hide spinner
function hideSpinner() {
    document.querySelector('.spinner').style.display = 'none';
    document.querySelector('.overlay').style.display = 'none';
}

const render_gerne = function (current_gerne, sub_gerne) {
    async function handleOnClick(id) {
        addParamURL('gerneId', id)
        const {current_gerne, sub_gerne} = await fetchGerne(id)
        margin += 10
        if (sub_gerne.length) {
            render_gerne(current_gerne, sub_gerne)
        } else {
            if (margin > 0) margin -= 10
            document.querySelector('.selected-filter').classList.remove("selected-filter")
            document.getElementById(id).classList.add("selected-filter")
        }
    }

    async function handleRemoveElement(elements) {
        showSpinner()
        requestAnimationFrame(() => {
            elements.forEach(parent => {
                if (parent) {
                    parent.remove();  // Remove each parent element from the DOM
                }
            });
        });
    }

    async function handleParentOnclick(elements, id) {
        addParamURL('gerneId', id)
        const {current_gerne, sub_gerne} = await fetchGerne(id)
        let rmElement = []
        elements.forEach(e => {
            if (e.id >= id) {
                rmElement.push(e.parentNode)
                if (margin > 0) margin -= 10
            }
        })
        await handleRemoveElement(rmElement)
        hideSpinner()


        render_current_gerne(current_gerne, margin)
        render_sub_gerne(sub_gerne, handleOnClick, margin)
    }

    render_parent_gerne(handleParentOnclick, margin)
    render_current_gerne(current_gerne, margin)
    render_sub_gerne(sub_gerne, handleOnClick, margin)
}

const render_parent_gerne = function (handleParentOnclick, margin) {
    const parent = document.querySelector(".parent-gerne")
    const current = document.querySelector(".current-gerne").lastElementChild
    if (current) {
        parent.insertAdjacentHTML("beforeend",
            `<li style="margin-left: ${margin}px"><span id="${current.id ? current.id : 1}" class="parent-gerne-item">${current.textContent}</span></li>`)

        const elements = document.querySelectorAll('.parent-gerne-item')
        elements.forEach(el => {
            el.removeEventListener("click", handleParentOnclick)
            el.addEventListener('click', e => handleParentOnclick(elements, e.target.id))
        })
    }
}

const render_current_gerne = function (book_gerne, margin) {
    const el = document.querySelector(".current-gerne")
    el.innerHTML = `
         <span style="margin-left: ${margin + 10}px" id="${book_gerne[0].id}" class="selected-filter">${book_gerne[0].name}</span>
    `
    el.children[0].addEventListener('click', e => {
        document.querySelector('.selected-filter').classList.remove("selected-filter")
        e.target.classList.add("selected-filter")
    })
}
const render_sub_gerne = function (books_gerne, handleOnclick, margin) {
    const el = document.querySelector(".children-gerne")
    const html = books_gerne.map(b => `
         <li style="margin-left: ${margin + 20}px"><span class="sub-item" id="${b.id}">${b.name}</span></li>`)
        .join("")
    el.innerHTML = html
    const elements = document.querySelectorAll('.sub-item')
    elements.forEach(e => e.addEventListener('click', () => handleOnclick(e.id)))
}

const addParamURL = function (param, value) {
    currentUrl.searchParams.set(param, value)
    window.history.pushState({}, '', currentUrl);
}
const deleteParamURL = function (param) {
    currentUrl.searchParams.delete(param);
    window.history.pushState({}, '', currentUrl);
}

async function app_start() {
    const {current_gerne, sub_gerne} = await fetchGerne(1)
    render_gerne(current_gerne, sub_gerne)
    handleSelectedFileter()
    handleSelectOrder('pagination', 'limit')
    handleSelectOrder('order', 'order')
}

//INVOKE FUNCTION
const sub_item = document.querySelectorAll(".sub-item")
sub_item.forEach(s => {
    async function handleOnClick(id) {
        const {current_gerne, sub_gerne} = await fetchGerne(id)
        render_gerne(current_gerne, sub_gerne)
    }

    s.addEventListener("click", () => handleOnClick(s.id))
})

function handleSelectedFileter() {
    const price_filter = document.querySelectorAll('.checkbox')

    function handleDeleteFilter(checkboxEl) {
        const filter = document.querySelector('.delete-filter')
        if (filter)
            filter.addEventListener('click',
                () => {
                    deleteParamURL('minPrice');
                    deleteParamURL('maxPrice');
                    document.querySelector('.price-filter').remove()
                    checkboxEl.classList.remove('checkbox-checked')
                    window.history.pushState({}, '', currentUrl);
                })
    }

    const prev = document.querySelector('.checkbox-checked')
    handleDeleteFilter(prev)

    price_filter.forEach(p => p.addEventListener("click", (e) => {
        const prev = document.querySelector('.checkbox-checked')
        const listFiler = document.querySelector('.filter-list')
        p.classList.add('checkbox-checked')


        window.history.pushState({}, '', currentUrl);
        if (prev && prev !== p) {
            addParamURL('minPrice', p.getAttribute("minPrice"))
            addParamURL('maxPrice', p.getAttribute("maxPrice"))
            listFiler.insertAdjacentHTML('beforeend',
                `<li class="filter-item price-filter">
                <span >Giá ${p.textContent}</span>
                <a class="cursor-pointer delete-filter ml-1"><i class="fa-solid fa-x"></i></a>
              </li>`)
            prev.classList.remove('checkbox-checked')
            document.querySelector('.price-filter').remove()
        } else if (prev === p) {
            deleteParamURL('minPrice');
            deleteParamURL('maxPrice');
            prev.classList.remove('checkbox-checked')
            document.querySelector('.price-filter').remove()
        } else {
            addParamURL('minPrice', p.getAttribute("minPrice"))
            addParamURL('maxPrice', p.getAttribute("maxPrice"))
            listFiler.insertAdjacentHTML('beforeend',
                `<li class="filter-item price-filter">
                <span >Giá ${p.textContent}</span>
                <a class="cursor-pointer delete-filter ml-1"><i class="fa-solid fa-x"></i></a>
              </li>`)
        }

        handleDeleteFilter(p)


        window.history.pushState({}, '', currentUrl);
    }))
}

function handleSelectOrder(nameNode, param) {
    const els = document.querySelector(`.dropdown-menu-${nameNode}`)
    els.querySelectorAll('.dropdown-item').forEach(
        el => el.addEventListener('click', () => {
            const value = el.getAttribute('value')
            document.querySelector(`.dropdown-toggle-${nameNode}`).textContent
                = el.textContent
            currentUrl.searchParams.set(param, value)
            window.history.pushState({}, '', currentUrl);
        })
    )
}

app_start()

