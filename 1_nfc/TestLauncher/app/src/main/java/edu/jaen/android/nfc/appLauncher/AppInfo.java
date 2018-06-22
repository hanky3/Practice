package edu.jaen.android.nfc.appLauncher;

public class AppInfo {

	private String appTitle;
	private String appPackage;

	public AppInfo() {
	}

	public AppInfo(String appTitle, String appPackage) {
		this.appTitle = appTitle;
		this.appPackage = appPackage;
	}

	public String getAppTitle() {
		return appTitle;
	}

	public void setAppTitle(String appTitle) {
		this.appTitle = appTitle;
	}

	public String getAppPackage() {
		return appPackage;
	}

	public void setAppPackage(String appPackage) {
		this.appPackage = appPackage;
	}

	@Override
	public String toString() {
		return getAppTitle();
	}

}
