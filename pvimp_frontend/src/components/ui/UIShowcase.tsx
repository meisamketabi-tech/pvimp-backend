import React from "react";
import "./UIShowcase.css";

import {
    Alert,
    Badge,
    Button,
    Card,
    FileUpload,
    Input,
    Select,
    Textarea
} from "./index";

export default function UIShowcase() {
    return (
        <div className="pv-ui-showcase">

            <h1>مجموعه کامپوننت‌های رابط کاربری PVIMP</h1>

            <Card title="ورودی‌های فرم">

                <div className="pv-ui-showcase-grid">

                    <Input
                        label="نام"
                        placeholder="نام را وارد کنید"
                    />

                    <Select
                        label="نوع مرکز"
                        options={[
                            {
                                label: "مرکز دولتی",
                                value: "1"
                            },
                            {
                                label: "مرکز خصوصی",
                                value: "2"
                            }
                        ]}
                    />

                    <Textarea
                        label="توضیحات"
                        placeholder="توضیحات را وارد کنید"
                    />

                    <FileUpload
                        label="فایل"
                        hint="فایل موردنظر را انتخاب کنید"
                    />

                </div>

            </Card>

            <Card title="دکمه‌ها">

                <div className="pv-ui-showcase-actions">

                    <Button>
                        ثبت
                    </Button>

                    <Button variant="secondary">
                        ویرایش
                    </Button>

                    <Button variant="danger">
                        حذف
                    </Button>

                </div>

            </Card>

            <Card title="اعلان‌ها">

                <div className="pv-ui-showcase-actions">

                    <Badge>
                        فعال
                    </Badge>

                    <Alert>
                        اطلاعات با موفقیت ثبت شد.
                    </Alert>

                </div>

            </Card>

        </div>
    );
}