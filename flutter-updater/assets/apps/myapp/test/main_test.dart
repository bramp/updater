import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:myapp/main.dart';

void main() {
  testWidgets('App renders HomePage', (tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('Hello, World!'), findsOneWidget);
    expect(find.byType(Scaffold), findsOneWidget);
  });
}
