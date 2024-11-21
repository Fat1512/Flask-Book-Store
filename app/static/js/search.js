//API
const BOOK_GERNE_API = '/api/v1/bookGerne'
const BOOK_API = '/api/v1/book'
const currentUrl = new URL(window.location);
const VND = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});
// DECLARE VARIABLE
var margin = 0

//DECALE FUNCTION
async function fetchGerne(id) {
    const res = await fetch(`${BOOK_GERNE_API}?gerneId=${id}`)
    if (!res.ok) throw Error("Failed getting book gerne")
    const data = await res.json()
    return data
}

async function fetchBook(params) {
    const res = await fetch(`${BOOK_API}/?${params}`)
    if (!res.ok) throw Error("Failed getting book")
    const data = await res.json()
    console.log(data)
    return data
}

function showSpinner() {
    document.querySelector('.spinner').style.display = 'block';
    document.querySelector('.overlay').style.display = 'block';

}

async function render_book(params) {
    const {books, current_page, pages} = await fetchBook(params)
    const el = document.querySelector('.list-book')
    console.log(books)
    if (!books.length) {
        const el_pg = document.querySelector('.pagination')
        el.innerHTML = `
             <p class="label-warning">
                Không có sản phẩm phù hợp với tìm kiếm của bạn
             </p>
        `
        el_pg.innerHTML = ""
        return
    }


    const html = books.map(b => `
        <a href="#" class="card col-md-3">
        <span class="discount text-white">10%</span>
        <img class="card-img-top"
             src="${b.images.length ? b.images[0].image_url : null}"
             alt="Card image">
        <div class="card-body p-0">
            <p class="card-text">${b.title}</p>
            <p class="text-primary font-weight-bold mb-1">${VND.format(b.price)}</p>
            <p class="text-secondary text-decoration-line-through mb-1">${b.price}</p>
        </div>
        <div class="rating">
            <i class="fa-regular fa-star"></i>
            <i class="fa-regular fa-star"></i>
            <i class="fa-regular fa-star"></i>
            <i class="fa-regular fa-star"></i>
            <i class="fa-regular fa-star"></i>
        </div>
    </a>
    `).join("")
    el.innerHTML = html
    render_pagination(current_page, pages)
}

const render_pagination = function (current_page, pages) {
    const el = document.querySelector('.pagination')
    const html = []
    const prevButton = current_page === 1 ? null : `
           <li class="page-item">
                <a class="page-link prev-button" href="#" aria-label="Previous">
                    <i class="fa-solid fa-arrow-left"></i>
                </a>
            </li>
    `
    html.push(prevButton)
    for (let i = 1; i < pages + 1; i++) {
        html.push(`
         <li class="page-item item-button">
            <a class="page-link ${i === current_page ? 'active' : ""}"  href="#" aria-label=${i}>
                ${i}
            </a>
        </li>
       `)

    }
    const nextButton = current_page === pages ? null : ` 
         <li class="page-item next-button">
            <a class="page-link" href="#" aria-label="Next">
                <i class="fa-solid fa-arrow-right"></i>
            </a>
        </li>
    `
    html.push(nextButton)
    el.innerHTML = html.join("")
    document.querySelectorAll('.item-button').forEach(item => {
        item.addEventListener('click', () => {
            addParamURL('page', item.textContent.trim())
            render_book(currentUrl.toString().split("?")[1])
        })
    })
    document.querySelector('.next-button').addEventListener('click', (e) => {
        next_page = currentUrl.searchParams.get('page') ? parseInt(currentUrl.searchParams.get('page')) + 1 : 2
        console.log(currentUrl.searchParams.get('page'))
        addParamURL('page', next_page)
        render_book(currentUrl.toString().split("?")[1])
    })
    document.querySelector('.prev-button') && document.querySelector('.prev-button').addEventListener('click', (e) => {
        prev_page = parseInt(currentUrl.searchParams.get('page')) - 1
        addParamURL('page', prev_page)
        render_book(currentUrl.toString().split("?")[1])
    })
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
        render_book(currentUrl.toString().split("?")[1])
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
        render_book(currentUrl.toString().split("?")[1])
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
                    deleteParamURL('page')
                    document.querySelector('.price-filter').remove()
                    checkboxEl.classList.remove('checkbox-checked')
                    window.history.pushState({}, '', currentUrl);
                    render_book(currentUrl.searchParams.toString().split("?")[1])
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
            deleteParamURL("page")
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
            deleteParamURL("page")
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
        render_book(currentUrl.toString().split("?")[1])
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
            deleteParamURL('page')
            window.history.pushState({}, '', currentUrl);
            render_book(currentUrl.toString().split("?")[1])
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // Adds smooth scrolling
            });
        })
    )
}


async function app_start() {
    const gerne_id = currentUrl.searchParams.get("gerneId")
        ? parseInt(currentUrl.searchParams.get("gerneId")) : 1
    const {current_gerne, sub_gerne} = await fetchGerne(1)
    render_gerne(current_gerne, sub_gerne)
    handleSelectedFileter()
    handleSelectOrder('pagination', 'limit')
    handleSelectOrder('order', 'order')
    render_book(currentUrl.toString().split("?")[1])
}

app_start()

