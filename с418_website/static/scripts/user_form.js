// ��������� ���������� ������� submit �� ����� � id="userForm"
document.getElementById("userForm").addEventListener("submit", function (e) {
    e.preventDefault();  // �������� ����������� �������� �����, ����� �� ���� ������������ ��������

    const form = e.target;  // �������� ������ �� �����
    const formData = new FormData(form);  // �������� ������ ����� � ������� FormData (����-��������)
    const data = new URLSearchParams(formData);  // ����������� FormData � URL-��������� (��� x-www-form-urlencoded)

    // ���������� POST-������ �� ������ �� ������ /active_users
    fetch("/active_users", {
        method: "POST",  // ����� �������
        headers: { "Content-Type": "application/x-www-form-urlencoded" },  // ��������� ������ ������ �����
        body: data  // ���� ������� � ������ �����
    })
        .then(response => response.json())  // ����������� ����� �� ������� � JSON
        .then(res => {
            const errorMsg = document.getElementById("formError");  // �������� ������� ��� ������ ������
            if (res.error) {
                // ���� ���� ������ �� ������� � ������� ��������� �� ������
                errorMsg.textContent = res.error;
            } else {
                // ���� ������ ��� � ������� ��������� �� ������
                alert("User was successfully added!");

                // ������� ���� �����
                document.getElementById("username").value = "";
                document.getElementById("description").value = "";
                document.getElementById("date").value = "";
                document.getElementById("telephone").value = "";

                // ������� ��������� �� ������
                errorMsg.textContent = ""

                //location.reload(); // ������������ ��������
            }
        })
        .catch(err => {
            // ���� �������� ������ ��� ���������� ������� � ������� ��������� �� ������
            alert("There was an error: " + err);
        });
});