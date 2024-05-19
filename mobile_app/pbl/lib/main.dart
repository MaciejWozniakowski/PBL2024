import 'dart:convert';
import 'dart:developer';

import 'joystick.dart';
import 'package:flutter/material.dart';
import 'package:ssh2/ssh2.dart';

void main() {
  runApp(const UtilsApp());
}

class UtilsApp extends StatelessWidget {
  const UtilsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Jetracer Utils App',
      home: MyHomePage(title: 'Jetracer Steering App'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _lidar = false;
  bool _camera = false;
  bool _jetracer = false;
  bool _roscore = false;

  Future<void> _handleLidar() async {
    setState(() {
      _lidar = !_lidar;
    });

    if (_lidar) {
      // Adres IP oraz dane uwierzytelniające
      const String host = '10.44.25.20';
      const int port = 22;
      const String username = 'jetson';
      const String password = 'jetson';

      var client = SSHClient(
        host: host,
        port: port,
        username: username,
        passwordOrKey: password,
      );

      try {
        String result = '';
        result = await client.connect() ?? 'Null result';
        if (result == "session_connected") {
          result = await client.startShell(
                  ptyType: "xterm",
                  callback: (dynamic res) {
                    setState(() {
                      result += res;
                    });
                  }) ??
              'Null result';

          if (result == "shell_started") {
            print(await client.writeToShell("screen -mS lidar_screen\n"));
            print(await client.writeToShell("screen -ls\n"));
            print(
                await client.writeToShell("roslaunch jetracer lidar.launch\n"));
          }
        }
      } on Exception catch (e) {
        log('Error: $e');
      }
    }
  }

  Future<void> _handleCamera() async {
    setState(() {
      _camera = !_camera;
    });
    if (_camera) {
      // Adres IP oraz dane uwierzytelniające
      const String host = '10.44.25.20';
      const int port = 22;
      const String username = 'jetson';
      const String password = 'jetson';

      var client = SSHClient(
        host: host,
        port: port,
        username: username,
        passwordOrKey: password,
      );

      try {
        String result = '';
        result = await client.connect() ?? 'Null result';
        if (result == "session_connected") {
          result = await client.startShell(
                  ptyType: "xterm",
                  callback: (dynamic res) {
                    setState(() {
                      result += res;
                    });
                  }) ??
              'Null result';

          if (result == "shell_started") {
            print(await client.writeToShell("screen -mS camera_screen\n"));
            print(await client.writeToShell("screen -ls\n"));
            print(await client
                .writeToShell("roslaunch jetracer csi_camera.launch\n"));
          }
        }
      } on Exception catch (e) {
        log('Error: $e');
      }
    }
  }

  Future<void> _handleRoscore() async {
    setState(() {
      _roscore = !_roscore;
    });
    if (_camera) {
      // Adres IP oraz dane uwierzytelniające
      const String host = '10.44.25.20';
      const int port = 22;
      const String username = 'jetson';
      const String password = 'jetson';

      var client = SSHClient(
        host: host,
        port: port,
        username: username,
        passwordOrKey: password,
      );

      try {
        String result = '';
        result = await client.connect() ?? 'Null result';
        if (result == "session_connected") {
          result = await client.startShell(
                  ptyType: "xterm",
                  callback: (dynamic res) {
                    setState(() {
                      result += res;
                    });
                  }) ??
              'Null result';

          if (result == "shell_started") {
            print(await client.writeToShell("screen -mS camera_screen\n"));
            print(await client.writeToShell("screen -ls\n"));
            print(await client.writeToShell("roscore\n"));
          }
        }
      } on Exception catch (e) {
        log('Error: $e');
      }
    }
  }

  Future<void> _handleJetracer() async {
    setState(() {
      _jetracer = !_jetracer;
    });
    if (_jetracer) {
      // Adres IP oraz dane uwierzytelniające
      const String host = '10.44.25.20';
      const int port = 22;
      const String username = 'jetson';
      const String password = 'jetson';

      var client = SSHClient(
        host: host,
        port: port,
        username: username,
        passwordOrKey: password,
      );

      try {
        String result = '';
        result = await client.connect() ?? 'Null result';
        if (result == "session_connected") {
          result = await client.startShell(
                  ptyType: "xterm",
                  callback: (dynamic res) {
                    setState(() {
                      result += res;
                    });
                  }) ??
              'Null result';

          if (result == "shell_started") {
            print(await client.writeToShell("screen -mS jetracer_screen\n"));
            print(await client.writeToShell("screen -ls\n"));
            print(await client
                .writeToShell("roslaunch jetracer jetracer.launch\n"));
          }
        }
      } on Exception catch (e) {
        log('Error: $e');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromRGBO(232, 223, 202, 1.0),
      appBar: AppBar(
        backgroundColor: const Color.fromRGBO(26, 77, 46, 1.0),
        title: Text(
          widget.title,
          style: const TextStyle(color: Colors.white),
        ),
        iconTheme: const IconThemeData(color: Colors.white),
        actions: <Widget>[
          PopupMenuButton(
            itemBuilder: (BuildContext context) {
              return <PopupMenuEntry>[
                const PopupMenuItem(
                  enabled: false,
                  child: Text('Uruchom komponenty sterujące'),
                ),
                const PopupMenuDivider(),
                CheckedPopupMenuItem(
                  value: _roscore,
                  checked: _roscore,
                  onTap: _handleRoscore,
                  child: const Text('Roscore'),
                ),
                CheckedPopupMenuItem(
                  value: _jetracer,
                  checked: _jetracer,
                  onTap: _handleJetracer,
                  child: const Text('Jetracer'),
                ),
                CheckedPopupMenuItem(
                  value: _lidar,
                  checked: _lidar,
                  onTap: _handleLidar,
                  child: const Text('Lidar'),
                ),
                CheckedPopupMenuItem(
                  value: _camera,
                  checked: _camera,
                  onTap: _handleCamera,
                  child: const Text('Kamera'),
                ),
              ];
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Container(
                  margin: const EdgeInsets.all(15.0),
                  padding: const EdgeInsets.all(3.0),
                  decoration: BoxDecoration(
                    color: const Color.fromRGBO(79, 111, 82, 1.0),
                    border: Border.all(
                      color: Colors.black,
                      width: 2.0,
                    ),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.arrow_upward),
                    onPressed: () {
                      // Obsłuż kliknięcie przycisku w górę
                    },
                    color: Colors.black,
                  ),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                Container(
                  margin: const EdgeInsets.all(15.0),
                  padding: const EdgeInsets.all(3.0),
                  decoration: BoxDecoration(
                    color: const Color.fromRGBO(79, 111, 82, 1.0),
                    border: Border.all(
                      color: Colors.black,
                      width: 2.0,
                    ),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.arrow_back),
                    onPressed: () {
                      // Obsłuż kliknięcie przycisku wstecz
                    },
                    color: Colors.black,
                  ),
                ),
                Container(
                  margin: const EdgeInsets.all(15.0),
                  padding: const EdgeInsets.all(3.0),
                  decoration: BoxDecoration(
                    color: const Color.fromRGBO(79, 111, 82, 1.0),
                    border: Border.all(
                      color: Colors.black,
                      width: 2.0,
                    ),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.arrow_forward),
                    onPressed: () {
                      // Obsłuż kliknięcie przycisku do przodu
                    },
                    color: Colors.black,
                  ),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Container(
                  margin: const EdgeInsets.all(15.0),
                  padding: const EdgeInsets.all(3.0),
                  decoration: BoxDecoration(
                    color: const Color.fromRGBO(79, 111, 82, 1.0),
                    border: Border.all(
                      color: Colors.black,
                      width: 2.0,
                    ),
                  ),
                  child: IconButton(
                    icon: const Icon(Icons.arrow_downward),
                    onPressed: () {
                      // Obsłuż kliknięcie przycisku w dół
                    },
                    color: Colors.black,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
