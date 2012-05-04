package com.memorykloud.Activities;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.ByteArrayBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.memorykloud.R;
import com.memorykloud.Http.HttpPackage;
import com.memorykloud.Http.HttpRequestTask;
import com.memorykloud.Http.IHttpCallback;

import android.app.*;
import android.graphics.Bitmap;
import android.graphics.Bitmap.CompressFormat;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

public class MomentManagerActivity extends Activity implements
		IHttpCallback<Void> {

	protected Bitmap _captureImage;
	protected int _imageHeight;
	protected int[] _kloudIdSpinnerIndex; // index: SpinnerIndex; value:
											// kloudletId

	protected String _url_get_all_kloudlet;
	protected String _url_post_pic;
	private HttpRequestTask _httpTask;

	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_momentmgr);

		// retrieve the bundle from the previous activity
		Bundle bundle = getIntent().getExtras();
		_captureImage = bundle.getParcelable("capture_image");

		InitializePage();

	}

	/** Called when the page is initialized **/
	private void InitializePage() {
		/* Get Value from XML resource */
		_imageHeight = Integer.parseInt(this.getString(R.string.IMAGE_HEIGHT));
		_url_get_all_kloudlet = this.getString(R.string.URL_GET_KlOUDLETS);
		_url_post_pic = this.getString(R.string.URL_POST_PICTURE);

		// show the thumb-nail picture
		// http://stackoverflow.com/questions/9461283/thumbnail-of-an-image-from-resources
		Float width = new Float(_captureImage.getWidth());
		Float height = new Float(_captureImage.getHeight());
		Float ratio = width / height;
		Bitmap thumbnail = Bitmap.createScaledBitmap(_captureImage,
				(int) (_imageHeight * ratio), _imageHeight, false);

		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		thumbnail.compress(Bitmap.CompressFormat.JPEG, 100, baos);
		ImageView im_thumbnail = (ImageView) findViewById(R.id.thumbnail);
		im_thumbnail.setImageBitmap(thumbnail);

		// populate the kloudlet list and default to current kloudlet
		GetAllKloudlets();
	}

	private void GetAllKloudlets() {
		// populate All the kloudlets
		this._httpTask = new HttpRequestTask(this, this,
				HttpRequestTask.HTTPType.GET);
		List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
		nameValuePairs.add(new BasicNameValuePair("id", "all"));

		this._httpTask.SetPackage(_url_get_all_kloudlet,
				new HttpPackage(_url_get_all_kloudlet, nameValuePairs));
		_httpTask.execute();
	}

	public void SaveContent_Click(View view) {
		Spinner spinner = (Spinner) findViewById(R.id.spinnerkloudlet);
		int kloudlet_id = _kloudIdSpinnerIndex[spinner
				.getSelectedItemPosition()];
		// For debugging: Toast.makeText(ContentManagerActivity.this, "" +
		// kloudlet_id, Toast.LENGTH_SHORT).show();

		// TODO: current UserId, hard code it for now
		int user_id = 882;

		EditText descp = (EditText) findViewById(R.id.description);
		String moment_descp =  descp.getText().toString();
		CreateMomentWithPicture(user_id, kloudlet_id, moment_descp);

	}

	private void CreateMomentWithPicture(int uId, int kId, String description) {
		// Create a moment with picture
		try {
			// http://vikaskanani.wordpress.com/2011/01/11/android-upload-image-or-file-using-http-post-multi-part/
			ByteArrayOutputStream bos = new ByteArrayOutputStream();
			_captureImage.compress(CompressFormat.JPEG, 100, bos);
			byte[] data = bos.toByteArray();
			ByteArrayBody bab = new ByteArrayBody(data, "upload.jpg");

			// upload
			this._httpTask = new HttpRequestTask(this, this,
					HttpRequestTask.HTTPType.POSTMULTIPART);

			MultipartEntity multipartEntity = new MultipartEntity(
					HttpMultipartMode.BROWSER_COMPATIBLE);
			multipartEntity.addPart("file", bab);
			multipartEntity.addPart("kid", new StringBody("" + kId));
			multipartEntity.addPart("uid", new StringBody("" + uId));
			multipartEntity.addPart("descp", new StringBody("" + description));

			this._httpTask.SetPackage(_url_post_pic, new HttpPackage(
					_url_post_pic, multipartEntity));
			_httpTask.execute();
		} catch (Exception e) {
			// handle exception here
			Log.e(e.getClass().getName(), e.getMessage());
		}
	}

	@Override
	public void onHttpTaskComplete(Void noParams) {
		HttpPackage pkg= null;
		Object result = null;
		
		pkg = this._httpTask.GetPackage(_url_get_all_kloudlet);
		if (pkg != null ){
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof JSONArray) {
					// create an adapter for the spinner
					ArrayAdapter<CharSequence> adapter = new ArrayAdapter<CharSequence>(
							this, android.R.layout.simple_spinner_item);
					adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);

					// get all the kloudlets and fill in the adapter
					JSONArray jArray = (JSONArray) result;
					_kloudIdSpinnerIndex = new int[jArray.length()];
					for (int i = 0; i < jArray.length(); i++) {
						JSONObject json_data;
						try {
							json_data = jArray.getJSONObject(i);
							adapter.add(json_data.getString("NAME"));
							_kloudIdSpinnerIndex[i] = json_data.getInt("ID");
						} catch (JSONException e) {
							Log.e("log_tag",
									"Error processing JSON " + e.toString());
						}
					}

					// show them in the spinner
					Spinner spinner_kloudlet = (Spinner) findViewById(R.id.spinnerkloudlet);
					spinner_kloudlet.setAdapter(adapter);
				}
			}
		}
			
		
		pkg = this._httpTask.GetPackage(_url_post_pic);
		if (pkg != null ){
			result = pkg.get_response();
			if (result != null) {
				if (result instanceof String) {
					// For debugging purpose
					// Toast.makeText(MomentManagerActivity.this, result.toString(), Toast.LENGTH_SHORT).show();
				}
				this.finish();
			}
		}
		
		this._httpTask.ClearPackage();

	}

}
