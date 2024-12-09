#include <crow/app.h>
#include <curl/curl.h>
#include <iostream>
#include <nlohmann/json.hpp>
#include <string>

using json = nlohmann::json;

// Function to make a POST request to the Ollama server
std::string request_ollama(const std::string &prompt) {
  CURL *curl;
  CURLcode res;
  std::string response_string;
  curl_global_init(CURL_GLOBAL_DEFAULT);
  curl = curl_easy_init();

  if (curl) {
    std::string url =
        "http://localhost:11434/api/generate"; // Ollama server URL
    json payload = {
        {"model", "qwen:0.5b"}, {"prompt", prompt}, {"stream", false}};
    std::string json_data = payload.dump();

    // Set the URL and payload
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data.c_str());

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    curl_easy_setopt(
        curl, CURLOPT_WRITEFUNCTION,
        +[](char *ptr, size_t size, size_t nmemb, std::string *data) {
          data->append(ptr, size * nmemb);
          return size * nmemb;
        });
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response_string);

    res = curl_easy_perform(curl);

    if (res != CURLE_OK) {
      std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res)
                << std::endl;
      return "Error: Could not get response from Ollama API";
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();
  }
  try {
    json json_response = json::parse(response_string);
    std::string response_text = json_response["response"];
    return response_text;
  } catch (const std::exception &e) {
    std::cerr << "Error parsing response: " << e.what() << std::endl;
    return "Error: Failed to parse response from Ollama API";
  }
}

int main() {
  crow::SimpleApp app;

  CROW_ROUTE(app, "/api/chat")
      .methods("POST"_method)([](const crow::request &req) {
        auto body = json::parse(req.body);
        std::string prompt = body["prompt"];

        std::string response = request_ollama(prompt);

        return crow::response{response};
      });

  app.port(8080).multithreaded().run();

  return 0;
}
