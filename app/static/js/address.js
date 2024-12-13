const PROVINCE_API = `https://provinces.open-api.vn/api/p/`
const DISTRICT_API = `https://provinces.open-api.vn/api/d/`
const WARD_API = 'https://provinces.open-api.vn/api/w/'
const ACCOUNT_API = '/api/v1/account/address'
const fetchProvince = async function () {
    try {
        const res = await fetch(PROVINCE_API)
        if (!res.ok) throw new Error("Something wrong")
        if (res['status'] === 200)
            return res.json()
    } catch (error) {
        console.log(error)
    }
}
const addAddress = async function (data) {
    try {
        const response = await fetch(`${ACCOUNT_API}`, {
            method: 'POST', // HTTP PUT method
            body: data
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json()
    } catch (error) {
        showToast(error.message, true)
    }
}
const fethDistrict = async function (code) {
    try {
        const res = await fetch(DISTRICT_API)
        if (!res.ok) throw new Error("Something wrong")
        if (res['status'] === 200) {
            const data = await res.json()
            return data.filter(item => item.province_code === code)
        }
    } catch (error) {
        console.log(error)
    }
}
const fethWard = async function (code) {
    try {
        const res = await fetch(WARD_API)
        if (!res.ok) throw new Error("Something wrong")
        if (res['status'] === 200) {
            const data = await res.json()
            return data.filter(item => item.district_code === code)
        }
    } catch (error) {
        console.log(error)
    }
}


const handleInputProvinceChange = debounce(async e => {
    const children = provinceElement.children
    for (let i = 0; i < children.length; i++) {
        const value = e.target.value
        const provinceName = children[i].innerText
        if (provinceName.toLowerCase().includes(value.toLowerCase())) {
            children[i].style = 'display:block'
        } else {
            children[i].style = 'display:none'
        }
    }

}, 1000)
const handleInputDistrictChange = debounce(async e => {
    const children = districtElement.children
    for (let i = 0; i < children.length; i++) {
        const value = e.target.value
        const districtName = children[i].innerText
        if (districtName.toLowerCase().includes(value.toLowerCase())) {
            children[i].style = 'display:block'
        } else {
            children[i].style = 'display:none'
        }
    }

}, 1000)
const handleInputWardChange = debounce(async e => {
    const children = wardElement.children
    for (let i = 0; i < children.length; i++) {
        const value = e.target.value
        const wardName = children[i].innerText
        if (wardName.toLowerCase().includes(value.toLowerCase())) {
            children[i].style = 'display:block'
        } else {
            children[i].style = 'display:none'
        }
    }

}, 1000)
const provinceElement = document.querySelector('.dropdown-province')
const districtElement = document.querySelector('.dropdown-district')
const wardElement = document.querySelector('.dropdown-ward')
const inputProvince = document.querySelector('input[name="dropdown-province"]')
const inputDistrict = document.querySelector('input[name="dropdown-district"]')
const inputWard = document.querySelector('input[name="dropdown-ward"]')
const inputName = document.querySelector('input[name="name"]')
const inputPhone = document.querySelector('input[name="phone"]')
const modalAddAddress = document.querySelector('.modal-address')
const addressLisst = document.querySelector('.address-list')
var pronvince = ''
var district = ''
var ward = ''
inputProvince.addEventListener('input', (e) => handleInputProvinceChange(e))
inputDistrict.addEventListener('input', e => handleInputDistrictChange(e))
inputDistrict.addEventListener('input', e => handleInputWardChange(e))

function handleCloseForm() {
    modalAddAddress.style = 'display:none'
    pronvince = ''
    district = ''
    ward = ''
    inputProvince.value = ''
    inputDistrict.value = ''
    inputWard.value = ''
    inputPhone.value = ''
    inputName.value = ''
    inputDistrict.disabled = true
    inputWard.disabled = true
}

const showToast = function (message, isError) {
    const color = isError ? 'var(--red)' : "#6cbf6c"
    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "center", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: color,
        }
    }).showToast()
}
modalAddAddress.querySelectorAll('.close-form').forEach(
    el => el.addEventListener('click', e => {
        handleCloseForm()
    }))
modalAddAddress.querySelector('.form-address').addEventListener('submit', (e) => {
        e.preventDefault()
        const formData = new FormData(modalAddAddress.querySelector('.form-address'))
        let flag = true
        formData.forEach((value, key) => {

            if (!value) {
                flag = false
                document.querySelector(`input[name='${key}']`).style = 'border: 1px solid red'
            }
        });
        if (flag) {
            addAddress(formData).then(res => {
                if (res['status'] === 200) {
                    handleCloseForm()
                    showToast("Thêm địa chỉ thành công", false)
                    const data = res['data']
                    addressLisst.insertAdjacentHTML('beforeend',`
                        <li class="address-item d-flex">
                            <div class="address-infor">
                                <div class="address-card d-flex justify-content-between align-items-start">
                                    <div class="address-info d-flex align-items-center">
                                        <span class="name">${data['fullname']}</span>
                                        <span class="phone">|${data['phone_number']}</span>
                                    </div>

                                </div>
                                <p class="address m-0 mt-2"> ${data['address']}</p>
                                <p class="address m-0 mb-2"> ${data['province']}</p>
                            </div>
                            <div class="address-btn-controll d-flex">
                                <p class="mr-3 cursor-pointer font-weight-bold text-primary">Cập nhật</p>
                                <p class="text-primary cursor-pointer font-weight-bold">Xóa</p>
                            </div>
                        </li>
                    `)
                }
            })
        }


    }
)
const btnAddAddress = document.querySelector('.btn-add-address')
btnAddAddress.addEventListener('click', () => {
    modalAddAddress.style = 'display:flex'
})
modalAddAddress.querySelector('.modal-body').addEventListener('click', (e) => {
    const elementsToCheck = [inputProvince, inputWard, inputDistrict, provinceElement, districtElement, wardElement];

    if (!elementsToCheck.some(element => element.contains(e.target))) {
        // Handle the case where the target is not contained in any element
        inputProvince.value = pronvince
        inputDistrict.value = district
        inputWard.value = ward
    }
})

async function handleOnClickProvince(code, content) {
    pronvince = content
    inputProvince.value = content
    inputDistrict.disabled = false
    await renderDistrict(code)
}

async function handleOnclickDistrict(code, content) {
    district = content
    inputDistrict.value = content
    inputWard.disabled = false
    await renderWard(code)
}

function handleOnClickWard(content) {
    ward = content
    inputWard.value = content
}

async function renderProvice() {
    const data = await fetchProvince()
    provinceElement.innerHTML = data.map(province => `
          <span onclick="handleOnClickProvince(${province.code},'${province.name}')" class="dropdown-item" value='${province.code}'>${province.name}</span>
    `).join('')
}

async function renderDistrict(code) {
    const data = await fethDistrict(code)

    districtElement.innerHTML = data.map(district => `
        <span onclick="handleOnclickDistrict(${district.code},'${district.name}')" class="dropdown-item" value='${district.code}'>${district.name}</span>
    `).join('')

}

async function renderWard(code) {
    const data = await fethWard(code)
    wardElement.innerHTML = data.map(ward => `
          <span onclick="handleOnClickWard('${ward.name}')" class="dropdown-item" 
          value='${ward.code}'>${ward.name}</span>
    `).join('')
}

renderProvice()
