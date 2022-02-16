import 'dart:io';

class AdMobService {

  String getAdMobAppId() {
    if (Platform.isAndroid) {
      return "";
    } else if (Platform.isIOS) {
      return "";
    }
    return null;
  }

  String getUpcomingAdId() {
    if (Platform.isAndroid) {
      return "";
    } else if (Platform.isIOS) {
      return "";
    }
    return null;
  }

}