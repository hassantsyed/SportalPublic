import 'package:flutter/material.dart';

class LeagueModel extends ChangeNotifier {
  final int lid;
  final String name;
  final Icon icon;

  LeagueModel(this.lid, this.name, this.icon);
}