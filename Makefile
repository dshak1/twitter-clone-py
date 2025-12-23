CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2
LDFLAGS := -pthread

APP_SRC := cpp/app.cpp
SERVER_SRC := cpp/server.cpp

APP_BIN := cpp/app
SERVER_BIN := cpp/twitter_server

.PHONY: all cpp app server run-server stop-server run-pyserver stop-pyserver clean

all: $(APP_BIN) $(SERVER_BIN)

$(APP_BIN): $(APP_SRC)
	$(CXX) $(CXXFLAGS) $< -o $@

$(SERVER_BIN): $(SERVER_SRC)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $< -o $@

app: $(APP_BIN)

server: $(SERVER_BIN)

run-server: $(SERVER_BIN)
	./$(SERVER_BIN) > server_cpp.log 2>&1 & echo $$! > server_pid && sleep 0.1 && lsof -i :8080 || true

stop-server:
	@if [ -f server_pid ]; then kill `cat server_pid` || true; rm -f server_pid; fi

run-pyserver:
	python3 py/flask_server.py > server.log 2>&1 & echo $$! > py_server_pid

stop-pyserver:
	@if [ -f py_server_pid ]; then kill `cat py_server_pid` || true; rm -f py_server_pid; fi

clean:
	-rm -f $(APP_BIN) $(SERVER_BIN) server_cpp.log server.log server_pid py_server_pid
