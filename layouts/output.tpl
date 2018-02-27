%include layouts/header

<div class="content-wrapper">
  <div class="row">
    <h3 class="text-info">File Output Page</h3>
  </div>
  <div class="row">
    <div class="col-12 grid-margin">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">File Output</h4>
          <div>
            % for element in ratOutput:
                <p>{{element}}</p>
            % end
          </div>
        </div>
      </div>
    </div>
  </div>
</div>


%include layouts/footer
