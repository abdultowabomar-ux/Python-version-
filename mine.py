import flet as ft
import sys
import io
import traceback

def main(page: ft.Page):
    page.title = "Omar IDE - محرر المهندس عمر"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800
    page.padding = 20

    # عنوان التطبيق
    header = ft.Text("Omar Python IDE 🐍", size=28, weight="bold", color=ft.colors.BLUE_200)

    # خانة كتابة الكود - صممتها لتكون مناسبة لشاشة الموبايل
    code_input = ft.TextField(
        label="اكتب كود بايثون هنا...",
        multiline=True,
        min_lines=12,
        max_lines=15,
        text_style=ft.TextStyle(font_family="monospace", size=14),
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_ACCENT,
        hint_text="مثال:\nimport math\nprint(math.sqrt(16))"
    )

    # مكان عرض النتائج
    output_display = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    
    def run_code(e):
        output_display.controls.clear()
        page.update()
        
        # تحويل المخرجات للواجهة بدل الترمينال
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            # تنفيذ الكود
            exec(code_input.value, {})
            result = new_stdout.getvalue()
            output_display.controls.append(ft.Text(result if result else "تم التنفيذ بنجاح (لا توجد مخرجات صريحة)", color=ft.colors.GREEN_400))
        except Exception:
            # في حالة الخطأ، نعرض الـ Traceback كامل عشان المبرمج يفهم الغلط فين
            error_msg = traceback.format_exc()
            output_display.controls.append(ft.Text(error_msg, color=ft.colors.RED_400, size=12))
        finally:
            sys.stdout = old_stdout
            page.update()

    # أزرار التحكم
    run_btn = ft.ElevatedButton(
        "تشغيل الكود 🚀",
        on_click=run_code,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
            padding=20
        ),
        width=float("inf")
    )

    clear_btn = ft.TextButton(
        "مسح الشاشة",
        on_click=lambda _: [setattr(code_input, "value", ""), page.update()],
        color=ft.colors.GREY_400
    )

    # بناء الواجهة
    page.add(
        header,
        ft.Text("محرر أكواد يدعم العمليات الرياضية والمنطقية", size=12, color=ft.colors.GREY_500),
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        code_input,
        ft.Row([run_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([clear_btn], alignment=ft.MainAxisAlignment.END),
        ft.Divider(),
        ft.Text("المخرجات (Console Output):", size=16, weight="bold"),
        ft.Container(
            content=output_display,
            bgcolor=ft.colors.BLACK,
            padding=10,
            border_radius=10,
            expand=True,
            border=ft.border.all(1, ft.colors.GREY_800)
        )
    )

ft.app(target=main)
