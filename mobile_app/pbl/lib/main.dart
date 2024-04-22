import 'package:flutter/material.dart';

void main() {
  runApp(const UtilsApp());
}

class UtilsApp extends StatelessWidget {
  const UtilsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Jetracer Utils App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Jetracer Steering App'),
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

  void _handleLidar() {
    setState(() {
      _lidar = !_lidar;
    });
    // Tutaj możesz umieścić kod, który ma być wykonywany po wybraniu opcji 1
  }

  void _handleCamera() {
    setState(() {
      _lidar = !_lidar;
    });
    // Tutaj możesz umieścić kod, który ma być wykonywany po wybraniu opcji 1
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 27, 154, 59),
        title: Text(widget.title),
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
                  ),
                ),
                Container(
                  margin: const EdgeInsets.all(15.0),
                  padding: const EdgeInsets.all(3.0),
                  decoration: BoxDecoration(
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
