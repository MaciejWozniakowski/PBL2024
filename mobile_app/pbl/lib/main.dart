import 'dart:developer';

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

  Future<void> _handleLidar() async {
    setState(() {
      _lidar = !_lidar;
    });

    if (_lidar) {
      // Adres IP oraz dane uwierzytelniające
      const String host = 'to be filled in';
      const int port = 22;
      const String username = 'jetson';
      const String password = 'jetson';

      final ssh = SSHClient(
        host: host,
        port: port,
        username: username,
        passwordOrKey: password,
      );

      try {
        await ssh.connect();
        String? result = await ssh.execute('ls'); // Tu wpisz swoją komendę SSH
        log('Result: $result');
      } on Exception catch (e) {
        log('Error: $e');
      } finally {
        await ssh.disconnect();
      }
    }
  }

  void _handleCamera() {
    setState(() {
      _camera = !_camera;
    });
    // Tutaj możesz umieścić kod, który ma być wykonywany po wybraniu opcji 2
  }

  void _handleJetracer() {
    setState(() {
      _jetracer = !_jetracer;
    });
    // Tutaj możesz umieścić kod, który ma być wykonywany po wybraniu opcji 3
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
