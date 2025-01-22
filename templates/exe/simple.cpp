#include <iostream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>

// Подключаем библиотеку Winsock
#pragma comment(lib, "Ws2_32.lib")

int main() {
    const std::string DOMAIN_NAME = "{{DOMAIN_NAME}}"; // Имя домена
    const int PORT = {{PORT}};                        // Порт
    const std::string USER_ID = "{{USER_ID}}";        // Идентификатор пользователя

    const std::string endpoint = "/api/executable_file_runned/?q=" + USER_ID;
    const std::string host = DOMAIN_NAME + ":" + std::to_string(PORT);

    // Создание тела и заголовков запроса
    const std::string request =
        "POST " + endpoint + " HTTP/1.1\r\n" +
        "Host: " + host + "\r\n" +
        "Content-Length: 0\r\n" +  // Указываем, что тела у запроса нет
        "Connection: close\r\n" +
        "\r\n";

    // Инициализация Winsock
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "Ошибка: не удалось инициализировать Winsock" << std::endl;
        return 1;
    }

    // Создаем сокет
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Ошибка: не удалось создать сокет" << std::endl;
        WSACleanup();
        return 1;
    }

    // Настройка адреса сервера
    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);

    // Преобразование доменного имени в IP-адрес
    if (inet_pton(AF_INET, DOMAIN_NAME.c_str(), &server_addr.sin_addr) <= 0) {
        std::cerr << "Ошибка: неверный адрес/формат доменного имени" << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Установка соединения с сервером
    if (connect(sock, (sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        std::cerr << "Ошибка: не удалось подключиться к серверу" << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Отправка запроса
    if (send(sock, request.c_str(), request.size(), 0) == SOCKET_ERROR) {
        std::cerr << "Ошибка: не удалось отправить запрос" << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Чтение ответа от сервера
    char buffer[1024];
    std::string response;
    int bytes_read;
    while ((bytes_read = recv(sock, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[bytes_read] = '\0';
        response += buffer;
    }

    if (bytes_read == SOCKET_ERROR) {
        std::cerr << "Ошибка: не удалось прочитать ответ от сервера" << std::endl;
    } else {
        std::cout << "Ответ от сервера:\n" << response << std::endl;
    }

    // Закрытие сокета
    closesocket(sock);
    WSACleanup();

    return 0;
}
