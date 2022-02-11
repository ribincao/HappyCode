- Server
	- Start()
	- Stop()
	- Serevr()
	- RegisterRouter(int, Router)
	- GetConnMgr() -> ConnectionManager
	- SetOnConnStart(func(Connection))
	- SetOnConnStop(func(Connection))
	- CallOnConnStart(Connection)
	- CallConnStop(Connection)
	- Codec() -> codec
	+ msgHandler
		- DoMsgHandler(Request)
		- RegisterRouter(int, Router)
		- StartWorkerPool()
		- SendMsgToTaskQueue(Request)
		+ apis  [int]Router
					- PreHandler()
					- Handler()
					- PostHandler()
		+ workerPoolSize
		+ taskQueue []chan Request
							- GetConnection()
							- GetData()
							- GetMsgID()
							+ conn Connection
							+ msg Message
	+ connectionManager
		- Add(Connection)
		- Remove(Connection)
		- Get(int) -> Connection
		- Len() -> int
		- ClearConnection()
		+ connections [int]Connection
							- Start()
							- Stop()
							- Context() -> Context
							- GetTcpConnection()
							- GetConnId()
							- RemoteAddr()
							- SendMsg()
							- SendBuffMsg()
							- SetProperty()
							- GeProperty()
							- RemoveProperty()
							+ TcpServer Server
							+ Conn
							+ ConnID
							+ MsgHandler
							+ ctx
							+ cancel
							+ msgChan
							+ msgBuffChan
							+ Mutex
							+ property [string]interface{}
							+ propertyLock
							+ isClosed bool
		+ connLock
	+ codec
		- Decode([] byte) -> Message
								- GetDataLen()
								- GetMsgId()
								- GetData()
								- SetMsgId()
								- SetData()
								- SetDataLen()
								+ DataLen
								+ ID
								+ Data []byte
		- Encode(Message) -> [] byte
		- GetHeadLen -> int
	+ onConnStart(Connection)
	+ onConnStop(Connection)
	+ name
	+ ip
	+ port
	+ version
