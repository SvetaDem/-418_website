// Добавляем обработчик события submit на форму с id="userForm"
document.getElementById("userForm").addEventListener("submit", function (e) {
    e.preventDefault();  // Отменяем стандартную отправку формы, чтобы не было перезагрузки страницы

    const form = e.target;  // Получаем ссылку на форму
    const formData = new FormData(form);  // Собираем данные формы в формате FormData (ключ-значение)
    const data = new URLSearchParams(formData);  // Преобразуем FormData в URL-параметры (для x-www-form-urlencoded)

    // Отправляем POST-запрос на сервер по адресу /active_users
    fetch("/active_users", {
        method: "POST",  // Метод запроса
        headers: { "Content-Type": "application/x-www-form-urlencoded" },  // Указываем формат данных формы
        body: data  // Тело запроса — данные формы
    })
        .then(response => response.json())  // Преобразуем ответ от сервера в JSON
        .then(res => {
            const errorMsg = document.getElementById("formError");  // Получаем элемент для вывода ошибок
            if (res.error) {
                // Если есть ошибка от сервера — выводим сообщение об ошибке
                errorMsg.textContent = res.error;
            } else {
                // Если ошибки нет — выводим сообщение об успехе
                alert("User was successfully added!");

                // Очищаем поля формы
                document.getElementById("username").value = "";
                document.getElementById("description").value = "";
                document.getElementById("date").value = "";
                document.getElementById("telephone").value = "";

                // Очищаем сообщение об ошибке
                errorMsg.textContent = ""

                //location.reload(); // перезагрузка страницы
            }
        })
        .catch(err => {
            // Если возникла ошибка при выполнении запроса — выводим сообщение об ошибке
            alert("There was an error: " + err);
        });
});