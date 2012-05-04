package com.memorykloud.Adapters;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Base64;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.View.OnClickListener;
import android.widget.BaseAdapter;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.memorykloud.R;

/*
 * This is the adapter that will write content into Content Page
 */
public class MomentAdapter extends BaseAdapter implements Filterable {
	private LayoutInflater _inflater;
	private Context _context;
	private JSONArray _jArray;

	public MomentAdapter(Context context) {
		// Cache the LayoutInflate to avoid asking for a new one each time.
		_inflater = LayoutInflater.from(context);
		this._context = context;
	}

	public void SetJSONArray(JSONArray jArray) {
		this._jArray = jArray;
	}

	/**
	 * Make a view to hold each row.
	 * 
	 * @see android.widget.ListAdapter#getView(int, android.view.View,
	 *      android.view.ViewGroup)
	 */
	@Override
	public View getView(final int position, View convertView, ViewGroup parent) {
		// A ViewHolder keeps references to children views to avoid
		// unneccessary calls
		// to findViewById() on each row.
		ViewHolder holder;

		// When convertView is not null, we can reuse it directly, there is
		// no need
		// to reinflate it. We only inflate a new View when the convertView
		// supplied
		// by ListView is null.

		convertView = _inflater.inflate(R.layout.mk_moment, null);

		// Creates a ViewHolder and store references to the two children
		// views
		// we want to bind data to.
		holder = new ViewHolder();
		holder.imageView = (ImageView) convertView.findViewById(R.id.picture);
		holder.usernameView = (TextView) convertView
				.findViewById(R.id.username);
		holder.metadataView = (TextView) convertView
				.findViewById(R.id.metadata);
		holder.descriptionView = (TextView) convertView.findViewById(R.id.text);

		convertView.setOnClickListener(new OnClickListener() {
			private int pos = position;

			@Override
			public void onClick(View v) {
				Toast.makeText(_context, "Click-" + String.valueOf(pos),
						Toast.LENGTH_SHORT).show();
			}
		});

		convertView.setTag(holder);

		// Bind the data efficiently with the holder.
		try {
			JSONObject json_data = _jArray.getJSONObject(position);
			holder.usernameView.setText(json_data.getString("CREATED_BY"));
			holder.metadataView.setText(json_data.getString("CREATED_ON"));
			String description = json_data.getString("TEXT");
			if (!description.equals("None"))
				holder.descriptionView.setText(description);
			else
				holder.descriptionView.setText("");
			String blob_str = json_data.getString("BLOBDATA");
			if (!blob_str.equals("None")) {
				int flags = Base64.DEFAULT;
				byte[] bin = Base64.decode(blob_str, flags);
				Bitmap bm = BitmapFactory.decodeByteArray(bin, 0, bin.length);
				holder.imageView.setImageBitmap(bm);
				//holder.imageView.getLayoutParams().height = 200;
				//notifyDataSetChanged();
			} else {
				holder.imageView.getLayoutParams().height = 5;
				holder.imageView.setImageDrawable(null);
				//notifyDataSetChanged();
			}

		} catch (JSONException e) {
			Log.e("log_tag", "Error processing JSON " + e.toString());
		}

		return convertView;
	}

	static class ViewHolder {
		TextView usernameView;
		ImageView imageView;
		TextView metadataView;
		TextView descriptionView;
		int momentId;
	}

	@Override
	public Filter getFilter() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public long getItemId(int position) {
		// TODO Auto-generated method stub
		return position;
	}

	@Override
	public int getCount() {
		// TODO Auto-generated method stub
		return _jArray.length();
	}

	@Override
	public Object getItem(int position) {
		// TODO Auto-generated method stub
		return null;
	}

}
