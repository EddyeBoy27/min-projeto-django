const pksList = []

async function orderList(event) {
    const { target } = event;
    event.preventDefault();
    const bodyAppend = document.getElementById('aside-container');
    const csrfToken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).getAttribute('value');
    const pk = target.getAttribute('value');
    const qntValue = document.getElementById(`qnt-container${pk}`)
    let apiResult;
    if (!pksList.includes(pk)) {
        apiResult = await axios.post(
            `http://127.0.0.1:8000/produtos/orders/add/${pk}/`,
            { data: {
                'csrfmiddlewaretoken': csrfToken,
            }},
        );
    } else if (pksList.includes(pk)) {
        apiResult = await axios.post(`http://127.0.0.1:8000/produtos/orders/update/${pk}/`);
    }
    bodyAppend.innerHTML += apiResult.data;
    pksList.push(pk);
}

async function increaseQnt({ target }) {
    return
}
