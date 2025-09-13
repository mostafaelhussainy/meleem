class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)  # 👈 give parent the message

err = AppException("hello", 400)


print(err.message)      # ✅ "hello"
print(err.status_code)  # ✅ 400
print(str(err))         # ❌ "" (empty string!)
print(Exception("Hi"))