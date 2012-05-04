package com.memorykloud.Activities;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;

import com.memorykloud.R;

import android.app.*;
import android.content.*;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.util.Log;
import android.util.TypedValue;
import android.view.*;
import android.widget.*;

import com.memorykloud.Adapters.*;
import com.memorykloud.Http.HttpPackage;
import com.memorykloud.Http.HttpRequestTask;
import com.memorykloud.Http.IHttpCallback;
import com.memorykloud.Sat.SatelliteMenu;
import com.memorykloud.Sat.SatelliteMenuItem;
import com.memorykloud.Sat.SatelliteMenu.SateliteClickedListener;

public class MomentViewerActivity extends ListActivity implements
		IHttpCallback<Void> {

	private MomentAdapter _adap;

	protected int _imageHeight;

	protected String _url_get_moments_by_kloudlet;
	private int _kloudlet_id;
	private String _kloudlet_name;
	private HttpRequestTask _httpTask;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_moment_viewer);

		// retrieve the bundle from the previous activity
		Bundle bundle = getIntent().getExtras();
		_kloudlet_id = bundle.getInt("kloudlet_id");
		_kloudlet_name = bundle.getString("kloudlet_name");

		InitializePage();

	}

	/** Called when the page is initialized **/
	private void InitializePage() {
		/* Variable Configuration */
		_imageHeight = Integer.parseInt(this.getString(R.string.IMAGE_HEIGHT));
		_url_get_moments_by_kloudlet = this
				.getString(R.string.URL_GET_MOMENTS_BY_KLOUDLETID);

		/* UI Configuration */
		InitializeSatelliteMenu();
		TextView title = (TextView) findViewById(R.id.title);
		title.setText(_kloudlet_name);

		/* HTTP queries */
		GetMomentsByKloudId();
	}

	private void InitializeSatelliteMenu() {
		SatelliteMenu menu = (SatelliteMenu) findViewById(R.id.menu);
		float distance = TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP,
				200, getResources().getDisplayMetrics());
		menu.setSatelliteDistance((int) distance);
		menu.setExpandDuration(500);
		menu.setCloseItemsOnClick(true);
		menu.setTotalSpacingDegree(90);

		List<SatelliteMenuItem> items = new ArrayList<SatelliteMenuItem>();
		items.add(new SatelliteMenuItem(6, R.drawable.menu_friend));
		items.add(new SatelliteMenuItem(5, R.drawable.menu_location));
		items.add(new SatelliteMenuItem(4, R.drawable.menu_audio));
		items.add(new SatelliteMenuItem(3, R.drawable.menu_thought));
		items.add(new SatelliteMenuItem(2, R.drawable.menu_pic));
		items.add(new SatelliteMenuItem(1, R.drawable.menu_kloudlet));
		menu.addItems(items);

		menu.setOnItemClickedListener(new SateliteClickedListener() {

			public void eventOccured(int id) {
				switch (id) {
				case 1: // kloudlet
					break;
				case 2: // picture
					
					startCameraActivity();
					break;
				case 3: // thought
					break;
				case 4: // audio
					break;
				case 5: // location
					break;
				case 6: // friend
					break;
				}
			}
		});
	}

	private void GetMomentsByKloudId() {
		// populate the moments list based on the given kloudletId

		this._httpTask = new HttpRequestTask(this, this,
				HttpRequestTask.HTTPType.GET);
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
		nameValuePairs.add(new BasicNameValuePair("kid", "" + _kloudlet_id));

		this._httpTask.SetPackage(_url_get_moments_by_kloudlet,
				new HttpPackage(_url_get_moments_by_kloudlet, nameValuePairs));
		_httpTask.execute();
	}

	protected void startCameraActivity() {
		Log.i("ContentViewerActivity", "startCameraActivity()");

		/*LayoutInflater inflater = (LayoutInflater)
	       this.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
	    PopupWindow pw = new PopupWindow(
	       inflater.inflate(R.layout.mk_pic_selection, null, false), 
	       100, 
	       100, 
	       true);
	    // The code below assumes that the root container has an id called 'main'
	    pw.showAtLocation(this.findViewById(R.id.actionbar), Gravity.CENTER, 0, 0);*/
	    
		Intent i = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
		startActivityForResult(i, 0);
	}

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {

		if (requestCode == 0 && resultCode == Activity.RESULT_OK) {
			Bitmap captureImage;
			captureImage = (Bitmap) data.getExtras().get("data");

			/*
			 * We can optionally write the file to a media library ContentValues
			 * values = new ContentValues(); values.put(MediaColumns.TITLE,
			 * "title"); values.put(ImageColumns.BUCKET_ID, "test");
			 * values.put(ImageColumns.DESCRIPTION, "test Image taken");
			 * values.put(MediaColumns.MIME_TYPE, "image/jpeg"); Uri uri =
			 * getContentResolver().insert(Media.EXTERNAL_CONTENT_URI, values);
			 * OutputStream outstream; try { outstream =
			 * getContentResolver().openOutputStream(uri);
			 * 
			 * captureImage.compress(Bitmap.CompressFormat.JPEG, 70, outstream);
			 * outstream.close(); } catch (FileNotFoundException e) { // } catch
			 * (IOException e) { // }
			 */

			// pass along the data for the next invoked activity
			Bundle bundle = new Bundle();
			bundle.putParcelable("capture_image", captureImage);

			Intent intent = new Intent(MomentViewerActivity.this,
					MomentManagerActivity.class);
			intent.putExtras(bundle);
			startActivityForResult(intent, 1);
		} else if (requestCode == 1) {
			GetMomentsByKloudId();
		}
	}

	@Override
	public void onHttpTaskComplete(Void noParams) {
		HttpPackage pkg = null;
		Object result = null;
		pkg = this._httpTask.GetPackage(_url_get_moments_by_kloudlet);
		if (pkg != null) {
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof JSONArray) {
					// create an adapter
					_adap = new MomentAdapter(this);
					// get the moments and fill in the adapter
					JSONArray jArray = (JSONArray) result;
					_adap.SetJSONArray(jArray);

					setListAdapter(_adap);
				}
			}
		}

		this._httpTask.ClearPackage();
	}

	public void Settings_Click(View view){
		startActivity(new Intent(MomentViewerActivity.this,
				SettingsActivity.class));
    } 
}
