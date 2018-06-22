package com.jaen.o2o.jaenpay;

import com.astuetz.PagerSlidingTabStrip;
import com.jaen.o2o.jaenpay.beacon.BeaconService;
import com.jaen.o2o.jaenpay.hce.AccountStorage;
import com.jaen.o2o.jaenpay.hce.CardEmulationFragment;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.LayerDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.preference.PreferenceFragment;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.ListFragment;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.Window;
import android.widget.Toast;

public class MainActivity extends FragmentActivity {
	// public class MainActivity extends Activity {

	// TAB 관련
	private PagerSlidingTabStrip tab;
	private ViewPager pager;

	// TAB의 각 page 관련 상수
	public final static int HOME_TAB = 0;
	public final static int CARD_TAB = 1;
	public final static int STORE_TAB = 2;
	public final static int SETTING_TAB = 3;

	private final static int CARD_UNREGI = 11;
	private final static int CARD_REGI = 12;
	private final static int SCAN_PERIOD = 10000;

	// TAB의 각 Fragment
	private static Fragment homeFrag;
	private static Fragment cardFrag;
	private static ListFragment storeFrag;
	private static Fragment settingFrag;

	private TabPagerAdapter tabPagerA;



	// 메인화면 로딩에 쓸 핸들러
	private Handler callH = new Handler();

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		// test
		// getWindow().requestFeature(Window.FEATURE_ACTION_BAR);

		setContentView(R.layout.activity_main);

		// 탭 프레그먼트 생성
		homeFrag = new HomeFragment(this);
		// cardFrag = new CardFragment(this);
		cardFrag = new CardEmulationFragment();
		storeFrag = new StoreFragment(this);
		settingFrag = new SettingFragment(this);

		// 탭 설정 초기화
		tab = (PagerSlidingTabStrip) this.findViewById(R.id.tabs);
		pager = (ViewPager) this.findViewById(R.id.pager);
		pager.setOffscreenPageLimit(0);

		tabPagerA = new TabPagerAdapter(getSupportFragmentManager());
		pager.setAdapter(tabPagerA);
		tab.setViewPager(pager);

		tab.setOnPageChangeListener(new OnPageChangeListener() {

			@Override
			public void onPageSelected(int arg0) {
				// 페이지가 바뀌는경우. onResume, onPause 두개에 필요한 것들을 여기다 쓰자
				Log.e("info", "index : " + arg0);
				switch (arg0) {
				case HOME_TAB:
					// ((MainTabSettingFrag) settingFrag).myPause();
					// ((MainTabHomeFrag) homeFrag).myResume();
					Toast.makeText(MainActivity.this, "HOME",
							Toast.LENGTH_SHORT).show();
					break;
				case CARD_TAB:
					// ((MainTabSettingFrag) settingFrag).myPause();
					// ((MainTabNewsFrag) newsFrag).myResume();
					Toast.makeText(MainActivity.this, "CARD",
							Toast.LENGTH_SHORT).show();

					break;
				case STORE_TAB:
					// ((MainTabSettingFrag) settingFrag).myPause();
					// ((MainTabAlarmFrag) alarmFrag).myResume();
					Toast.makeText(MainActivity.this, "STORE",
							Toast.LENGTH_SHORT).show();
					break;
				case SETTING_TAB:
					// ((MainTabSettingFrag) settingFrag).myResume();
					Toast.makeText(MainActivity.this, "SETTING",
							Toast.LENGTH_SHORT).show();
					break;

				default:
					break;
				}
			}

			@Override
			public void onPageScrolled(int arg0, float arg1, int arg2) {
			}

			@Override
			public void onPageScrollStateChanged(int arg0) {

			}
		});

		// 탭 시작위치 설정
		Intent i = getIntent();
		int startPosition = HOME_TAB;
		if (i != null)
			startPosition = i.getIntExtra("tabPosition", HOME_TAB);
		pager.setCurrentItem(startPosition);

		// 탭 색상 변경
		int color = Color.parseColor("#FFF4842D");
		tab.setIndicatorColor(color);
		tab.setTextColorResource(R.color.item_white);

		Drawable colorDrawable = new ColorDrawable(color);
		Drawable bottomDrawable = getResources().getDrawable(
				R.drawable.actionbar_bottom);
		LayerDrawable ld = new LayerDrawable(new Drawable[] { colorDrawable,
				bottomDrawable });
		getActionBar().setBackgroundDrawable(ld);
		getActionBar().hide();

    	// 비콘 서비스 START ----- 코드 구현...
		final Context ctx = this.getApplicationContext();
		callH.postDelayed(new Runnable() {
			@Override
			public void run() {
				startService(new Intent(ctx, BeaconService.class));
			}
		}, 1000);
	}

	@Override
	protected void onPause() {
		// TODO Auto-generated method stub
		super.onPause();
		// 메인액티비티가 사라질떄, 각 프레그먼트 생성값을 false로 초기화시킨다!
		// MainTabHomeFrag.isCreated = false;
		// MainTabNewsFrag.isCreated = false;
		// MainTabAlarmFrag.isCreated = false;
		// MainTabSettingFrag.isCreated = false;
	}

	@Override
	protected void onResume() {
		// TODO Auto-generated method stub
		super.onResume();

	}

	@Override
	protected void onDestroy() {
		// TODO Auto-generated method stub
		super.onDestroy();
		//비콘 서비스 종료 -----
		//코드 구현......
		stopService(new Intent(this, BeaconService.class));
	}

	// TAB 어댑터
	class TabPagerAdapter extends FragmentPagerAdapter {

		private String[] tabTitles = { "    home    ", "    card    ",
				"    store    ", "   setting   " };

		public TabPagerAdapter(FragmentManager fm) {
			super(fm);
		}

		@Override
		public Fragment getItem(int arg0) {

			Log.e("info", "209 ------ getItem call...  index : " + arg0);

			Fragment f;

			switch (arg0) {
			case HOME_TAB:
				f = homeFrag;
				break;
			case CARD_TAB:
				f = cardFrag;
				// Toast.makeText(MainActivity.this, "CARD_TAB 201.....",
				// Toast.LENGTH_SHORT).show();
				// f = new CardEmulationFragment();
				break;
			case STORE_TAB:
				f = storeFrag;
				break;
			case SETTING_TAB:
				f = settingFrag;
				break;

			default:
				f = homeFrag;
				break;
			}
			return f;
		}

		@Override
		public int getCount() {
			return tabTitles.length;
		}

		@Override
		public CharSequence getPageTitle(int position) {
			return tabTitles[position];
		}

	}

	// 최초 로딩설정
	// 2초 대기했다가(로딩이 끝나길) 메인화면을 뿌려준다.
	class MainLoadingThread extends Thread {
		@Override
		public void run() {
			try {
				sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			callH.sendEmptyMessage(0);
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		menu.add(Menu.NONE, CARD_REGI, Menu.NONE, R.string.card_add);
		menu.add(Menu.NONE, CARD_UNREGI, Menu.NONE, R.string.card_delete);
		return super.onCreateOptionsMenu(menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case CARD_REGI:
			showDialog(CARD_REGI);
			break;
		case CARD_UNREGI:
			showDialog(CARD_UNREGI);
			break;
		default:
			break;
		}
		return super.onOptionsItemSelected(item);
	}

	@Override
	protected Dialog onCreateDialog(int id) {
		AlertDialog.Builder dialog = new AlertDialog.Builder(this);
		switch (id) {
		case CARD_REGI:
			dialog.setIcon(android.R.drawable.ic_input_add)
					.setTitle("카드 등록")
					.setMessage("JaenPay 카드를 등록하시겠습니까?")
					.setPositiveButton("등 록",
							new DialogInterface.OnClickListener() {
								@Override
								public void onClick(DialogInterface dialog,
										int which) {
									// Scan Activity Start....
									Intent scanI = new Intent(
											getApplicationContext(),
											CardScanActivity.class);
									// scanI.setFlags(Intent.FLAG_ACTIVITY_NO_HISTORY);
									startActivity(scanI);
								}
							}).setNegativeButton("취 소", null);
			break;
		case CARD_UNREGI:
			dialog.setIcon(android.R.drawable.ic_input_add)
					.setTitle("카드 삭제")
					.setMessage("등록된 JaenPay 카드를 삭제하시겠습니까?")
					.setPositiveButton("삭  제",
							new DialogInterface.OnClickListener() {
								@Override
								public void onClick(DialogInterface dialog,
										int which) {
									AccountStorage.SetAccount(
											MainActivity.this, "00000000");
									Toast.makeText(MainActivity.this,
											"등록된 카드가 삭제되었습니다",
											Toast.LENGTH_SHORT).show();
								}
							}).setNegativeButton("취 소", null);
			break;

		default:
			break;
		}
		return dialog.create();
	}
}
