import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

/// The root application widget.
class MyApp extends StatelessWidget {
  /// Creates a new [MyApp].
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        colorSchemeSeed: Colors.blue,
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

/// The home page of the application.
class HomePage extends StatelessWidget {
  /// Creates a new [HomePage].
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My App'),
      ),
      body: const Center(
        child: Text('Hello, World!'),
      ),
    );
  }
}
